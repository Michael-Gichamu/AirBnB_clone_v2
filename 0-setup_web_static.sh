#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

if ! command -v nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

if [[ ! -d /data/web_static/releases/test ]]; then
  sudo mkdir -p /data/web_static/releases/test
fi
if [[ ! -d /data/web_static/shared ]]; then
  sudo mkdir -p /data/web_static/shared
fi

echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sfn /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i "46i\       location /hbnb_static/ {\n              alias /data/web_static/current/;\n      }" /etc/nginx/sites-enabled/default

sudo service nginx restart
