#!/bin/bash

while getopts ":u:e:p:d:" opt; do
  case $opt in
    u) uname="$OPTARG"
    ;;
    e) uemail="$OPTARG"
    ;;
    p) upassword="$OPTARG"
    ;;
    d) domain="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$uname" ]; then
  echo -e "\e[31mUsername is missing\e[0m"
  exit 2
fi

if [ -z "$upassword" ]; then
  echo -e "\e[31mPassword is missing\e[0m"
  exit 2
fi

if [ -z "$uemail" ]; then
  echo -e "\e[31mEmail is missing\e[0m"
  exit 2
fi

if [ -z "$domain" ]; then
  echo -e "\e[31mDomain is missing\e[0m"
  exit 2
fi

echo -e "\e[96mOpening up Firewall\e[0m"
sudo ufw allow 443
sudo ufw allow 80
sudo ufw allow 8000

echo -e "\e[96mInstalling dependencies\e[0m"
# > /dev/null &1
sudo pip3 uninstall -r requirements.txt -y
sudo apt-get install libjpeg-dev zlib1g-dev -y
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update
sudo apt-get install python3.9 python3-pip -y
sudo apt install nginx -y
sudo pip3 install -r requirements.txt
sudo apt install certbot python3-certbot-nginx -y

echo -e "\e[96mResetting workspace\e[0m"
sudo systemctl reset-failed fantasia || true
sudo systemctl stop fantasia || true
sudo systemctl disable fantasia || true
sudo rm /etc/systemd/system/fantasia.service || true

sudo rm -r /home/ubuntu/studio/fantasia/migrations
sudo rm /home/ubuntu/studio/db.sqlite3
sudo rm /etc/nginx/sites-available/fantasia
sudo rm /etc/nginx/sites-enabled/fantasia

echo -e "\e[96mCreating Fantasia Service\e[0m"
echo '[Unit]
Description=Gunicorn instance to serve studio fantasia
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/studio
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 django_fantasia.wsgi:application

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/fantasia.service

echo -e "\e[96mConfiguring Nginx with domain $domain\e[0m"
echo "server {
    listen 80;
    server_name $domain www.$domain;

    location / {
        include proxy_params;
        proxy_pass http://0.0.0.0:8000;
    }
}" > /etc/nginx/sites-available/fantasia
nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo certbot run -n --nginx -d "$domain" -d "www.$domain" -m "$uemail" --redirect
ln -s /etc/nginx/sites-available/fantasia /etc/nginx/sites-enabled

echo -e "\e[96mCreating database\e[0m"
python3 manage.py makemigrations fantasia
python3 manage.py sqlmigrate fantasia 0001
python3 manage.py migrate
sudo chown 777 db.sqlite3

echo -e "\e[96mCreating superuser\e[0m"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$uname', '$uemail', '$upassword')" | python3 manage.py shell
echo -e "\e[96mSuper User created with username $uname\e[0m"

echo -e "\e[96mStarting Fantasia Service\e[0m"
sudo systemctl start fantasia
sudo systemctl enable fantasia
sudo systemctl status fantasia
sudo systemctl status nginx