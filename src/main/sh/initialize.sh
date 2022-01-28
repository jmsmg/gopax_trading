#!/bin/bash
sudo apt update
sudo apt install -y python3 build-essential awscli supervisor python3-pip unzip nodejs
sudo pip3 install urllib3 requests boto3
sudo chmod u=rwx,g=rx,o=rx $HOME
curl -L https://raw.githubusercontent.com/c9/install/master/install.sh | bash

sudo cp src/main/conf/* /etc/supervisor/conf.d/
sudo supervisorctl reread
