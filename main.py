import asyncio
import websockets
import os
import logging as log
import kafka
import json
from aiokafka import AIOKafkaConsumer

from kafka.errors import NoBrokersAvailable
from kafka.admin.new_topic import NewTopic
import time
from concurrent.futures import ThreadPoolExecutor

WS_PORT = 3000  # default port
if "WS_PORT" not in os.environ:
    log.warning(f"WS_PORT env is not set defaulting port {WS_PORT}")
else:
    try:
        WS_PORT = int(os.environ["WS_PORT"])
    except:
        log.warning(f"WS_PORT env could not converted to int, defaulting to port {WS_PORT}")

KAFKA_TOPIC = "chat"
if "KAFKA_TOPIC" not in os.environ:
    log.warning(f"KAFKA_TOPIC env is not set defaulting {KAFKA_TOPIC}")
else:
    KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

KAFKA_BROKERS = "chat"
if "KAFKA_BROKERS" not in os.environ:
    log.warning(f"KAFKA_BROKERS env is not set defaulting {KAFKA_BROKERS}")
else:
    KAFKA_BROKERS = os.environ["KAFKA_BROKERS"]


async def add_to_kafka(data_str):
    try:
        data = json.loads(data_str)
        producer = kafka.KafkaProducer(bootstrap_servers=KAFKA_BROKERS,
                                       value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                       max_request_size=204857600,  # 200 MB
                                       max_block_ms=3600000)
        producer.send(KAFKA_TOPIC, value={
            "timestamp": data["timestamp"],
            "message": data["message"]
        }).get(timeout=3600)
    except Exception as e:
        log.exception("Could not sent to kafka", exc_info=e)


async def consumer_handler(websocket, path):
    async for message in websocket:
        log.warning("new message " + str(message))
        await add_to_kafka(message)


async def producer_handler(websocket, path):
    try:
        consumer: AIOKafkaConsumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=asyncio.get_event_loop(),
                                                      group_id=None,
                                                      bootstrap_servers=KAFKA_BROKERS,
                                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                                      consumer_timeout_ms=1000000, auto_offset_reset='earliest',
                                                      max_poll_interval_ms=2147483647)

        log.warning("consumer created")
        await consumer.start()
        await consumer.seek_to_beginning()
        try:
            async for message in consumer:
                await websocket.send(json.dumps(message.value))
        finally:
            # Will leave consumer group; perform autocommit if enabled.
            await consumer.stop()
    except NoBrokersAvailable as e:
        log.exception("No brokers available.", exc_info=e)
    except Exception as e:
        log.exception("Consumer init error ", exc_info=e)


async def chat(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))

    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))

    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()


while True:
    time.sleep(1)
    log.warning("Trying to connect to kafka")
    try:
        adminClient = kafka.KafkaAdminClient(bootstrap_servers=KAFKA_BROKERS)
        break
    except Exception as e:
        log.exception("Could not create admin client ", exc_info=e)

try:
    adminClient.create_topics([NewTopic(KAFKA_TOPIC, 1, 1)])
except Exception as e:
    log.exception("Could not create topic ", exc_info=e)

executor = ThreadPoolExecutor(max_workers=50)
start_server = websockets.serve(chat, "0.0.0.0", WS_PORT)

log.warning(f"Started ws server on port {WS_PORT}")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
