#!/bin/sh
APTGET=`which apt-get`
if [ -z "${APTGET}" ] ; then
    APTGET=`which yum`
fi
if [ -z "${APTGET}" ] ; then
    echo "FATAL ERROR: Failed to find apt-get or yum package installers"
    exit 1
fi
sudo ${APTGET} -y install xboxdrv
sudo ${APTGET} -y install lirc
sudo ${APTGET} -y install python-dev
sudo ${APTGET} -y install python-pip
sudo cp lircd.conf /etc/lirc/
sudo cp hardware.conf /etc/lirc/
sudo /etc/init.d/lirc restart
sudo cp xbox-daemon /usr/local/sbin
sudo chmod a+rx /usr/local/sbin/xbox-daemon
sudo python setup.py install
sudo cp 80-xbox360.rules /etc/udev/rules.d
sudo chmod u+rx /etc/udev/rules.d/80-xbox360.rules
echo "Finished installing Xbox-360 driver, you can now use the controller"
