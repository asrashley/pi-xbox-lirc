pi-xbox-lirc
============

This project allows you to control a YouView device from an Xbox360 controller
using a Raspberry Pi and an infra-red LED.

It works with both Humax and Huawei devices, although you need to configure
which device you are using, as the remote control protols differ.

Hardware Construction
---------------------
This project assumes that an infra-red emitting diode has been connected to
GPIO in P17 of the Raspberry Pi.

    +3v3 ------------
              |
             +-+
             | |   30R
             | |
             +-+
              |
              |
             +-+
             \ /  ->  Infrared emitter
             ---  ->
              |
              |
              |
    P17 --------------

I used an infrared LED from [maplin](http://maplin.co.uk/) (order code CY85G) and a 30 ohm
resiter (order code M30R) which gives a lousy range, but doesn't require a transistor
to drive the LED.

Automatic Install for Humax
---------------------------
To automatically download and install this package, and all of the packages
it depends upon, log in the Raspberry Pi and type:

    curl https://raw.github.com/asrashley/pi-xbox-lirc/master/install-humax.sh | sh

Automatic Install for Huawei
----------------------------
To automatically download and install this package, and all of the packages
it depends upon, log in the Raspberry Pi and type:

    curl https://raw.github.com/asrashley/pi-xbox-lirc/master/install-huawei.sh | sh

Manual Install
--------------
To perform the steps in the automatic installer one-by-one:

    git clone https://github.com/asrashley/pi-xbox-lirc.git
    cd pi-xbox-lirc
    sudo apt-get install git
    sudo apt-get install xboxdrv
    sudo apt-get install lirc
    sudo apt-get install python-dev
    sudo apt-get install python-pip

Edit src/xboxlirc/target.py to select which device (Humax / Huawei) you want
to control.

    sudo cp lircd.conf /etc/lirc/
    sudo cp hardware.conf /etc/lirc/
    sudo /etc/init.d/lirc restart

Enable auto-start
-----------------
The automatical installation scripts will also automatically enable the
driver when the gamepad is installed, but if you used the manual install
procedure, you will need to perform the following steps to enable auto-start:

    sudo python setup.py install
    sudo cp xbox-daemon /usr/local/sbin
    sudo chmod u+rx /usr/local/sbin/xbox-daemon
    sudo cp 80-xbox360.rules /etc/udev/rules.d
    sudo chmod u+rx /etc/udev/rules.d/80-xbox360.rules

Usage
-----
If auto-start has been enabled, when the Xbox controller is inserted in 
to a USB port, the Xbox driver and the lirc bridge should be auto-started

To manually start:

    /usr/bin/xboxdrv --trigger-as-button --id 0 --led 2 --deadzone 4000 --silent &
    python -m xboxlirc
