#!/bin/bash

sudo apt-get install -y curl

curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
sudo apt-get install -y nodejs

sudo npm install -g phantomjs
