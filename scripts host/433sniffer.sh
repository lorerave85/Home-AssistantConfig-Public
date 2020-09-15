# Locate: /etc/systemd/system


#!/bin/bash
sleep 5
rmmod dvb_usb_rtl28xxu
/usr/local/bin/rtl_433 -F json -M utc | mosquitto_pub -u mqtt -P lorenzo -t home/rtl_433 -l