# Locate: /usr/lib/cgi-bin

#!/bin/bash
echo "Content-Type: text/plain"
echo
sudo systemctl start loop_analog.service
exit 0