# Locate: /usr/lib/cgi-bin

#!/bin/bash
echo "Content-Type: text/plain"
echo
sudo systemctl stop loop_analog.service
exit 0