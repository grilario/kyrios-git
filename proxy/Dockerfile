FROM nginx:alpine

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=80
ENV APP_HOST=app
ENV APP_PORT=8000

USER root

RUN mkdir -p /http/static && \
  chmod 755 /http/static && \
  touch /etc/nginx/conf.d/default.conf && \
  chown nginx:nginx /etc/nginx/conf.d/default.conf && \
  chmod +x /run.sh

VOLUME [ "/http/static" ]

CMD [ "/run.sh" ]
