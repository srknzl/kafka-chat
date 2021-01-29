FROM alpine:3.13.0

RUN apk update --no-cache
RUN apk add --no-cache python3 py3-pip

RUN pip3 install kafka-python==2.0.2 websockets==8.1 asyncio==3.4.3 aiokafka==0.7.0

ENV PYTHONPATH=/opt/

WORKDIR /opt/

ENTRYPOINT ["python3",  "/opt/main.py"]
