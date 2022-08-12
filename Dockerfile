FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE 8000

# Installing git and liqpq to runtime dependencies
RUN apk --no-cache add git libpq && \
  git config --global init.defaultBranch main

# Install requirements and your dependencies
COPY requirements.txt /app/
RUN apk --no-cache add --virtual build-dependencies python3-dev libpq-dev build-base linux-headers && \
  pip install -r requirements.txt && \
  apk del build-dependencies

# Configs
COPY . /app/
COPY ./scripts /scripts

RUN adduser --disabled-password --no-create-home app && \
  mkdir -p /http/static && \
  chown -R app /http/static && \
  chmod -R 755 /http/static &&\   
  chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

# USER app

CMD ["run.sh"]

