FROM python:3.7.3-alpine3.9
MAINTAINER Bartosz Ligęza

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgres-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgres-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir /app
WORKDIR ./app /app

RUN adduser -D user
USER user