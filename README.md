pi-xbox-lirc
============

Drive Humax DTR-T1000 from an Xbox360 controller using a Raspberry Pi

Install
-------

    sudo apt-get install xboxdrv
    sudo apt-get install lirc
    sudo cp lircd.conf /etc/lirc/
    sudo cp hardware.conf /etc/lirc/
    sudo /etc/init.d/lirc restart
    sudo apt-get install python-dev
    sudo apt-get install python-pip
    sudo pip install evdev

Enable auto-start

    sudo cp xbox-daemon /usr/local/sbin
    sudo chmod u+rx /usr/local/sbin/xbox-daemon
    sudo cp xbox-lirc.py /usr/local/sbin
    sudo chmod a+r /usr/local/sbin/xbox-lirc.py
    sudo cp 80-xbox360.rules /etc/udev/rules.d
    sudo chmod u+rx /etc/udev/rules.d/80-xbox360.rules

Usage
-----
If auto-start has been enabled, when the Xbox controller is inserted in 
to a USB port, the Xbox driver and the lirc bridge should be auto-started

To manually start:

    /usr/bin/xboxdrv --trigger-as-button --id 0 --led 2 --deadzone 4000 --silent &
    python xbox-lirc.py

