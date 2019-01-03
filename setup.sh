#!/bin/bash

# Get script directory as DIR. From https://stackoverflow.com/a/246128
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Update and install dependencies
apt-get update
apt-get -y upgrade
rpi-update
apt-get -y install python3 nginx motion

# Make directory to store it all
mkdir /opt/usb-otg-webapi

# Setup USB
echo "dtoverlay=dwc2" | tee -a /boot/config.txt
echo "dwc2" | tee -a /etc/modules
echo "libcomposite" | tee -a /etc/modules

yes | cp -rf "${DIR}/usb-otg-driver.sh" /opt/usb-otg-webapi/usb-otg-driver.sh

chmod +x /opt/usb-otg-webapi/usb-otg-driver.sh

# Setup Python WebAPI
yes | cp -rf "${DIR}/main.py" /opt/usb-otg/webapi/main.py
yes | cp -rf "${DIR}/command_queue.py" /opt/usb-otg/webapi/command_queue.py
yes | cp -rf "${DIR}/keyboard_controller.py" /opt/usb-otg/webapi/keyboard_controller.py

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

yes | cp -rf "${DIR}/default-motion" /etc/default/motion
yes | cp -rf "${DIR}/motion.conf" /etc/motion/motion.conf

# Setup nginx
systemctl stop nginx

yes | cp -rf "${DIR}/nginx-conf" /etc/nginx/sites-available/default

systemctl start nginx

# Setup systemd
yes | cp -rf "${DIR}/usb-otg-driver.service" /opt/usb-otg-webapi/usb-otg-driver.service
yes | cp -rf "${DIR}/usb-otg-webapi.service" /opt/usb-otg-webapi/usb-otg-webapi.service

ln -f /opt/usb-otg-webapi/usb-otg-driver.service /lib/systemd/system/usb-otg-driver.service
ln -f /opt/usb-otg-webapi/usb-otg-webapi.service /lib/systemd/system/usb-otg-webapi.service

systemctl enable usb-otg-driver
systemctl enable usb-otg-webapi

# Reboot
reboot
