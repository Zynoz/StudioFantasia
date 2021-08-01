#!/bin/bash

red() {
  echo -e "\e[31m$1\e[0m"
}

blue() {
  echo -e "\e[96m$1\e[0m"
}

green() {
  echo -e "\e[32m$1\e[0m"
}

if [ "$(id -u)" != "0" ]; then
  red "Sorry, you are not sudo"
  exit 1
fi

while getopts ":u:e:p:d:" opt; do
  case $opt in
  u)
    uname="$OPTARG"
    ;;
  e)
    uemail="$OPTARG"
    ;;
  p)
    upassword="$OPTARG"
    ;;
  d)
    domain="$OPTARG"
    ;;
  \?)
    echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$uname" ]; then
  red "Username is missing"
  exit 2
fi

if [ -z "$upassword" ]; then
  red "Password is missing"
  exit 2
fi

if [ -z "$uemail" ]; then
  red "Email is missing"
  exit 2
fi

if [ -z "$domain" ]; then
  red "Domain is missing"
  exit 2
fi

blue "Resetting workspace"
sudo systemctl reset-failed fantasia || true
sudo systemctl stop fantasia || true
sudo systemctl disable fantasia || true
sudo rm /etc/systemd/system/fantasia.service || true
sudo apt-get purge nginx nginx-core nginx-common -y || true

sudo rm -r /home/ubuntu/studio/fantasia/migrations
sudo rm /home/ubuntu/studio/db.sqlite3
sudo rm /etc/nginx/sites-available/fantasia
sudo rm /etc/nginx/sites-enabled/fantasia
sudo rm -r /home/ubuntu/studio/media/
sudo rm /home/ubuntu/studio/gunicorn.access.log
sudo rm /home/ubuntu/studio/gunicorn.error.log

blue "Opening up Firewall"
sudo apt install ufw -y
sudo ufw enable
sudo ufw allow 443
sudo ufw allow 80
sudo ufw allow 22

#grep -qxF 'SECRET_KEY=""' ~/.profile || echo 'DJANGO_DEBUG=False' >>~/.profile

blue "Installing dependencies"
sudo apt-get install libjpeg-dev zlib1g-dev -y
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update
sudo apt-get install python3.9 python3-pip -y
sudo apt install nginx -y
sudo pip3 install -r requirements.txt
sudo apt install certbot python3-certbot-nginx -y

blue "Creating files and directories"
echo "If you can see me, then please contact the server administrator <a href=\"mailto: $uemail\">here</a>" >/usr/share/nginx/html/50x.html

sudo mkdir /home/ubuntu/studio/media
sudo mkdir /home/ubuntu/studio/media/gallery
sudo mkdir /home/ubuntu/studio/media/postimages
chown -R ubuntu:ubuntu /home/ubuntu/studio

blue "Creating Fantasia Service"
echo '[Unit]
Description=Gunicorn instance to serve studio fantasia
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/studio
ExecStart=/usr/local/bin/gunicorn --config /home/ubuntu/studio/gunicorn.conf.py django_fantasia.wsgi:application

[Install]
WantedBy=multi-user.target' >/etc/systemd/system/fantasia.service

blue "\e[96mConfiguring Nginx with domain $domain\e[0m"
echo "server {
    listen 80;
    server_name $domain www.$domain;

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
      root /usr/share/nginx/html/;
    }

    error_page 404 =200 /index.html;

    # Disable favicon.ico logging
    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    # Allow robots and disable logging
    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location /static/ {
#        autoindex on;
        alias /home/ubuntu/studio/static/;
    }

    location /media/ {
#        autoindex on;
        alias /home/ubuntu/studio/media/;
    }

    # Disable static content logging and set cache time to max
#    location ~* \.(jpg|jpeg|gif|png|css|js|ico|xml)$ {
#        access_log off;
#        log_not_found off;
#        expires max;
#    }

    # Deny access to htaccess and htpasswd files
    location ~ /\.ht {
        deny  all;
    }

    # Deny access to hidden files (beginning with a period)
    location ~ /\. {
        access_log off; log_not_found off; deny all;
    }

    location / {
        include proxy_params;
        proxy_pass http://0.0.0.0:8000;
    }
}" >/etc/nginx/sites-available/fantasia
nginx -t || exit 1
sudo systemctl restart nginx
sudo ln -s /etc/nginx/sites-available/fantasia /etc/nginx/sites-enabled
sudo certbot run -n --nginx -d "$domain" -d "www.$domain" -m "$uemail" --redirect --agree-tos

blue "Generating static files"
python3 manage.py collectstatic --noinput

blue "Creating database"
python3 manage.py makemigrations fantasia
python3 manage.py sqlmigrate fantasia 0001
python3 manage.py migrate
chown -R ubuntu:ubuntu /home/ubuntu/studio

blue "Creating superuser"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$uname', '$uemail', '$upassword')" | python3 manage.py shell
blue "Super User created with username $uname"

blue "Starting Fantasia Services"
sudo systemctl start fantasia
sudo systemctl enable fantasia
sudo systemctl status fantasia
sudo systemctl status nginx

statuscode=$(curl -s -o /dev/null -I -w "%{http_code}" "https://www.$domain")

if [ "$statuscode" = "200" ]; then
  green "Application Fantasia is up and running"
  green "You can access the Admin Dashboard at https://www.$domain/admin"
else
  red "https://www.$domain could not be reached. Please contact your system administrator"
fi
