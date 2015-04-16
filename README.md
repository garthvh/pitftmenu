## Simple PiTFT Touch Menu System

Simple touch menu for Raspberry Pi projects using the [3.5" Adafruit PiTFT](http://www.adafruit.com/products/2097) 480x320 touch screen.

Runs as a python script in the framebuffer without needing a desktop environment.

I have made a model b+ [Touch Pi](https://learn.adafruit.com/touch-pi-portable-raspberry-pi) 3D printed case for my screen and raspberry pi, and with a battery and [PowerBoost 500c](https://www.adafruit.com/product/1944) charger it makes a great base for raspberry pi projects.

Written using python and pygame the 3.5" screen is broken out into 8 menu items.

## Installation

    git clone https://github.com/garthvh/pitftmenu
    cd pitftmenu

The basic 8 Button Template can be run with the following command the buttons in this example simply print out the number of the button pushed and closes the menu:

![8 Button Menu Template](/images/menu_touchpi.jpg "8 Button Menu Template")

    sudo python menu_8button.py

My basic touch pi menu with a top label, buttons for Desktop, Terminal, Reboot and Shutdown.  This menu also displays your current ip address at the bottom.

![Touch Pi Menu](/images/menu_touchpi.jpg "Touch Pi Menu")

    sudo python menu_touchpi.py

### Reboot and Shutdown Buttons

If you want to enable the reboot and shutdown commands you will need to make the following updates

    sudo visudo

Add the following lines to the end of the file to target the www-data user

    www-data ALL=/sbin/shutdown
    www-data ALL=NOPASSWD: /sbin/shutdown

### Run menu at startup

If you want the script to run at startup, add a cron job

    sudo crontab -e

And add the following line to the bottom of the file

    @reboot python /home/pi/pitftmenu/menu_touchpi.py &

## References

The examples here are cobbled from other code below:

- https://github.com/5Volt-Junkie/RPi-Tron-Radio/blob/master/tron-radio.py
- http://richardhawthorn.com/?p=128
- http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/
- https://github.com/DoctorBud/raspberrypi-node/tree/176f7536d505de17b0d790855a836e0d2cb7d059/pitft-pygame
- https://learn.adafruit.com/pi-video-output-using-pygame/pygame-drawing-functions
- https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
- http://home.uktechreviews.com/Raspberry/Pi%20blog/files/pygame-menu.html
