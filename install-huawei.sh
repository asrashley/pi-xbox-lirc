#!/bin/sh
sudo apt-get update
sudo apt-get -y install git
git clone https://github.com/asrashley/pi-xbox-lirc.git
if [ -d pi-xbox-lirc ]; then
   cd pi-xbox-lirc 
   echo 'TARGET="huawei_talktalk"' > src/xboxlirc/target.py
   sh ./generic-install.sh
fi
