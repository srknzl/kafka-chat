FROM alpine:3.13.0

RUN apk update --no-cache
RUN apk add --no-cache python3 py3-pip

RUN pip3 install gunicorn kafka-python websockets asyncio

ENV PYTHONPATH=/opt/

WORKDIR /opt/

ENTRYPOINT ["python3",  "/opt/main.py"]
