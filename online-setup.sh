#!/bin/bash

# Update and install dependencies
apt-get update
apt-get -y upgrade
rpi-update
apt-get -y install curl python3 nginx motion

# Make directory to store it all
mkdir /opt/usb-otg-webapi

# Setup USB
echo "dtoverlay=dwc2" | tee -a /boot/config.txt
echo "dwc2" | tee -a /etc/modules
echo "libcomposite" | tee -a /etc/modules

curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/usb-otg-driver.sh > /opt/usb-otg-webapi/usb-otg-driver.sh

chmod +x /opt/usb-otg-webapi/usb-otg-driver.sh

# Setup Python WebAPI
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/main.py > /opt/usb-otg/webapi/main.py
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/command_queue.py > /opt/usb-otg/webapi/command_queue.py
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/keyboard_controller.py > /opt/usb-otg/webapi/keyboard_controller.py

chmod +x /opt/usb-otg-webapi/main.py

# Setup Camera
echo "bcm2835-v4l2" | tee -a /etc/modules

sed /boot/config.txt -i -e "s/^startx/#startx/"
sed /boot/config.txt -i -e "s/^fixup_file/#fixup_file/"
set_config_var start_x 1 /boot/config.txt
CUR_GPU_MEM=$(get_config_var gpu_mem /boot/config.txt)
if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]; then
  set_config_var gpu_mem 128 /boot/config.txt
fi

curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/etc-default-motion > /etc/default/motion
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/motion.conf > /etc/motion/motion.conf

# Setup nginx
systemctl stop nginx

curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/nginx-conf > /etc/nginx/sites-available/default

systemctl start nginx

# Setup systemd
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/usb-otg-driver.service > /opt/usb-otg-webapi/usb-otg-driver.service
curl https://raw.githubusercontent.com/Al-Azif/usb-otg-webapi/master/usb-otg-webapi.service > /opt/usb-otg-webapi/usb-otg-webapi.service

ln -f /opt/usb-otg-webapi/usb-otg-driver.service /lib/systemd/system/usb-otg-driver.service
ln -f /opt/usb-otg-webapi/usb-otg-webapi.service /lib/systemd/system/usb-otg-webapi.service

systemctl enable usb-otg-driver
systemctl enable usb-otg-webapi

# Reboot
reboot
