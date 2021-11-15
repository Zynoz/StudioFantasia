FROM python:3.8

RUN apt-get update && apt-get install nginx-full vim -y --no-install-recommends

RUN mkdir -p /opt/app
RUN mkdir -p /opt/storage
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/studio
RUN mkdir -p /opt/app/studio/static
RUN mkdir -p /opt/app/studio/media

COPY requirements.txt /opt/app/
WORKDIR /opt/app

RUN pip install -r requirements.txt
RUN apt-get install libjpeg-dev zlib1g-dev -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN add-apt-repository ppa:certbot/certbot -y
RUN apt install certbot python3-certbot-nginx -y
RUN chown -R www-data:www-data /opt/app

COPY start-server.sh /opt/app/
COPY studio /opt/app/studio/

RUN python3 studio/manage.py collectstatic --noinput
RUN python3 studio/manage.py makemigrations fantasia
RUN python3 studio/manage.py sqlmigrate fantasia 0001
RUN python3 studio/manage.py migrate --run-syncdb

#RUN touch /opt/storage/studio.sqlite3
#RUN chmod 664 /opt/app/storage/studio.sqlite3
#RUN chmod 664 /opt/app/studio/studio.sqlite3

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
RUN service nginx restart

EXPOSE 443
EXPOSE 8010
STOPSIGNAL SIGTERM
ENTRYPOINT ["bash", "/opt/app/start-server.sh"]
