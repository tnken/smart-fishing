#!/bin/bash

# This is setup script for initializing new raspberrypi zero
sudo apt update -y && apt upgrade -y

# Install Node.js from unofficial repo
# Because official repo do not support latest version for armv6l
# https://zenn.dev/mactkg/articles/5adc624787666c
sudo apt install -y npm
sudo npm i -g n
sudo N_NODE_MIRROR=https://unofficial-builds.nodejs.org/download/release/ n lts
node -v

#　App
npm create vite@latest -- sample-system --template react-ts
cd sample-system/
npm install

sudo echo WAIT:$(date +'%Y%m%d%H%M%S'): | sudo tee /srv/pi-camera/camera_mode.log