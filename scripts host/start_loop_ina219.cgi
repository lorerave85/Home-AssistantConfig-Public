# Locate: /usr/lib/cgi-bin

#!/bin/bash
echo "Content-Type: text/plain"
echo
sudo systemctl start loop_ina219.service
exit 0