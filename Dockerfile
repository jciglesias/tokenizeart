FROM python:3.11

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y make && \
    make

CMD [ "make", "run" ]