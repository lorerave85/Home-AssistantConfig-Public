# Locate: /etc/systemd/system


#!/bin/bash
while true; do
  # Do something
  /usr/bin/python3.7 /home/pi/plant_moisture_detector.py | mosquitto_pub -u mqtt -P lorenzo -t home/flower -l
  sleep 1;
done