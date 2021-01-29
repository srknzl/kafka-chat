# Real Time Kafka Chat

## Technologies

* Kafka is used for message streaming and storage. Python library names are kafka-python and aiokafka(for asyncio integration)
* Websocket is used for showing and sending messages without a reload need. (websockets package)
* Asyncio and aiokafka is used for asynchronous usage of Kafka.

## Running

* Install docker and docker-compose
* Run `docker-compose up -d` in root folder
* Go to localhost:8080 
* You can use more than one browser to test, or multiple tabs in a single browser
* Keep in mind that it can take 30 seconds for kafka and websocket server to start.

## SS
![](1.png)
