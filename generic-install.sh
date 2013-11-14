#!/bin/sh
sudo apt-get -y install git
sudo apt-get -y install xboxdrv
sudo apt-get -y install lirc
sudo apt-get -y install python-dev
sudo apt-get -y install python-pip
sudo cp lircd.conf /etc/lirc/
sudo cp hardware.conf /etc/lirc/
sudo /etc/init.d/lirc restart
sudo cp xbox-daemon /usr/local/sbin
sudo chmod u+rx /usr/local/sbin/xbox-daemon
sudo python setup.py install
sudo cp 80-xbox360.rules /etc/udev/rules.d
sudo chmod u+rx /etc/udev/rules.d/80-xbox360.rules
