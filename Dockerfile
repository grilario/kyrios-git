FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/

RUN apk --no-cache add git libpq \
  && apk --no-cache add --virtual build-dependencies python3-dev libpq-dev build-base \
  && pip install -r requirements.txt \
  && git config --global init.defaultBranch main \
  && apk del build-dependencies

COPY . /app/

