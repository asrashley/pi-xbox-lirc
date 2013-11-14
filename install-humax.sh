#!/bin/sh
git clone https://github.com/asrashley/pi-xbox-lirc.git
if [ -d pi-xbox-lirc ]; then
   cd pi-xbox-lirc 
   echo 'TARGET="humax"' > src/xboxlirc/target.py
   exec ./generic-install.sh
fi
