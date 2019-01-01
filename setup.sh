#!/bin/bash

# Update and install dependencies
apt-get update
apt-get -y upgrade
apt-get -y install python3 nginx

# Make directory to store it all
mkdir /opt/usb-otg-webapi

# Setup USB
echo "dtoverlay=dwc2" | tee -a /boot/config.txt
echo "dwc2" | tee -a /etc/modules
echo "libcomposite" | tee -a /etc/modules

cat << 'EOF' >> /opt/usb-otg-webapi/usb-otg-driver
#!/bin/bash

cd /sys/kernel/config/usb_gadget/
mkdir -p miskatonic
cd miskatonic
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "0123456789abcdef" > strings/0x409/serialnumber
echo "Miskatonic" > strings/0x409/manufacturer
echo "USB OTG via WebAPI" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC
EOF

chmod +x /opt/usb-otg-webapi/usb-otg-driver

# Setup Python WebAPI
cat << 'EOF' >> /opt/usb-otg-webapi/main.py

EOF

chmod +x /opt/usb-otg-webapi/main.py

# Setup Camera
echo "bcm2835-v4l2" | tee -a /etc/modules

# Setup nginx
systemctl stop nginx

cat << 'EOF' > /etc/nginx/sites-available/default
server {
  server_tokens off;

  charset UTF-8;

  chunked_transfer_encoding on;

  listen 80;

  root /var/www;
  index index.html;

  location ~ ^/api(|/|/.*)+$ {
    proxy_pass http://127.0.0.1:8888;
  }

  location / {
    try_files $uri $uri/ =404;
  }
}
EOF

systemctl start nginx

# Setup systemd
cat << 'EOF' >> /opt/usb-otg-webapi/usb_otg_driver.service
[Unit]
Description=USB OTG Driver
Wants=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
Group=root
WorkingDirectory=/opt/usb-otg-webapi
ExecStart=/opt/usb-otg-webapi/usb-otg-driver
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

cat << 'EOF' >> /opt/usb-otg-webapi/usb-otg-webapi.service
[Unit]
Description=USB OTG WebAPI
Wants=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
Group=root
WorkingDirectory=/opt/usb-otg-webapi
ExecStart=/opt/usb-otg-webapi/main.py --host "127.0.0.1" --port 8080
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

ln -f /opt/usb-otg-webapi/usb-otg-driver.service /lib/systemd/system/usb-otg-driver.service
ln -f /opt/usb-otg-webapi/usb-otg-webapi.service /lib/systemd/system/usb-otg-webapi.service

systemctl enable motion
systemctl enable usb-otg-driver
systemctl enable usb-otg-webapi

# Reboot
reboot
