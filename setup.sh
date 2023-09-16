#!/bin/bash

#
# This is setup script for initializing new raspberrypi zero
#

# AP settings
ip_addr="192.168.249.1/24"
ssid="PI_CAMERA_WIFI0"
pass="pi-camera0"

# Deps
apt update -y && apt upgrade -y
apt install -y python3-pip hostapd dnsmasq ffmpeg tmux git vim # todo: remove unnecessary pkgs
pip install --upgrade pip
pip install -r requirement.txt

# Network setup
echo -e "interface=wlan0\ndhcp-range=192.168.249.50,192.168.249.150,255.255.255.0,12h" >> /etc/dnsmasq.conf
echo -e "interface wlan0\n  static ip_address=$ip_addr\n  nohook wpa_supplicant" >> /etc/dhcpcd.conf
echo -e "ctrl_interface=/var/run/hostapd\nctrl_interface_group=0\ninterface=wlan0\ndriver=nl80211\nssid=$ssid\nhw_mode=g\ncountry_code=JP\nchannel=11\nieee80211d=1\nwmm_enabled=0\nmacaddr_acl=0\nauth_algs=1\nwpa=2\nwpa_passphrase=$pass\nwpa_key_mgmt=WPA-PSK\nrsn_pairwise=CCMP" > /etc/hostapd/hostapd.conf
echo "country=JP" >> /etc/wpa_supplicant/wpa_supplicant.conf
rfkill unblock wifi
systemctl unmask hostapd.service
systemctl enable hostapd.service

# App setup
mkdir -p /srv/pi-camera
sudo chmod 777 /srv/pi-camera
touch /srv/pi-camera/camera_mode.log
chmod 777 /srv/pi-camera/camera_mode.log
echo WAIT:$(date +'%Y%m%d%H%M%S'): >> /srv/pi-camera/camera_mode.log

# Run camera-app and pi-camera as background service

echo done.
echo Please reboot RaspberryPi to reflect this setup.
