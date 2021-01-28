FROM alpine:3.13.0

RUN apk update --no-cache
RUN apk add --no-cache npm

ADD . /opt

WORKDIR /opt

RUN npm i
RUN npm run build

ENTRYPOINT ["npm",  "start"]
