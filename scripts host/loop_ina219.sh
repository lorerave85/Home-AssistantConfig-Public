# Locate: /etc/systemd/system


#!/bin/bash
while true; do
  # Do something
  /usr/bin/python3.7 /home/pi/ina.py | mosquitto_pub -u mqtt -P lorenzo -t home/power_pi -l
  sleep 10;
done