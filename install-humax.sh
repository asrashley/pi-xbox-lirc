#!/bin/sh
sudo apt-get -y install git
git clone https://github.com/asrashley/pi-xbox-lirc.git
if [ -d pi-xbox-lirc ]; then
   cd pi-xbox-lirc 
   echo 'TARGET="humax"' > src/xboxlirc/target.py
   sh ./generic-install.sh
fi
