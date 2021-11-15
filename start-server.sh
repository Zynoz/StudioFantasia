#!/bin/env bash

if [ -n "$uname" ] && [ -n "$uemail" ] && [ -n "$upassword" ] && [ -n "$domain" ] ; then
    #todo fix ssl
    if [ -n "$runssl" ] ; then
      echo running certbot
      certbot run -n --nginx -d "$domain" -d "www.$domain" -m "$uemail" --redirect --agree-tos
    fi
    #todo check if db file is present; if present -> studio/manage.py migrate --database=PATH/TO/db.sqlite3
    #todo use mounted folders

    echo "Creating superuser"
    python3 studio/manage.py makemigrations fantasia
    python3 studio/manage.py migrate --run-syncdb
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('$uname', '$uemail', '$upassword')" | python3 studio/manage.py shell
    echo "Super User created with username $uname"

    #todo manage amount of workers with env variable?
    (cd studio; gunicorn studio.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
else
  echo "One or more variables are missing"
fi
nginx -g "daemon off;"
