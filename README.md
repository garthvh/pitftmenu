## Work in progress

Simple touch menu for Raspberry Pi projects using the [3.5" Adafruit PiTFT](http://www.adafruit.com/products/2097) 480x320 touch screen.

Runs as a python script in the framebuffer without a desktop environment.

I have made a model b+ [Touch Pi](https://learn.adafruit.com/touch-pi-portable-raspberry-pi) 3D printed case for my screen and raspberry pi, and with a battery and [PowerBoost 500c](https://www.adafruit.com/product/1944) charger it makes a great base for raspberry pi projects.

Written using python and pygame the 3.5" screen is broken out into 8  menu items.

### Installation

    git clone https://github.com/garthvh/pitftmenu
    cd pitftmenu

The basic 8 Button Template can be run with the following command the buttons in this example simply print out the number of the button pushed and closes the menu:

    sudo python menu_8button.py

My basic touch pi menu with a top label, buttons for Desktop, Exit, Reboot and Shutdown.  This screen also displays your current ip address.

    sudo python menu_touchpi.py

If you want to enable the reboot and shutdown commands you will need to make the following updates

    sudo visudo

Add the following lines to the end of the file to target the www-data user

    www-data ALL=/sbin/shutdown
    www-data ALL=NOPASSWD: /sbin/shutdown

### References

The examples here are cobbled from other code below:

- https://github.com/DoctorBud/raspberrypi-node/tree/176f7536d505de17b0d790855a836e0d2cb7d059/pitft-pygame
- https://learn.adafruit.com/pi-video-output-using-pygame/pygame-drawing-functions
- https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
- http://home.uktechreviews.com/Raspberry/Pi%20blog/files/pygame-menu.html
