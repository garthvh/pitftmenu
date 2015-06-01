# Simple PiTFT TouchPi Menu System

Simple touch menu for Raspberry Pi projects using the [3.5" Adafruit PiTFT](http://www.adafruit.com/products/2097) 480x320 touch screen.

Runs as a python script in the framebuffer without needing a desktop environment.

Featured on the adafruit blog for pi day:
<blockquote class="twitter-tweet" lang="en">
	<p lang="ht" dir="ltr">Simple PiTFT TouchPi Menu System <a href="https://twitter.com/hashtag/piday?src=hash">#piday</a> <a href="https://twitter.com/hashtag/raspberrypi?src=hash">#raspberrypi</a> <a href="https://twitter.com/Raspberry_Pi">@Raspberry_Pi</a> <a href="http://t.co/JT9CbFiwvz">http://t.co/JT9CbFiwvz</a></p>&mdash; adafruit industries (@adafruit) <a href="https://twitter.com/adafruit/status/596675973615071232">May 8, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I have made a model b+ [Touch Pi](https://learn.adafruit.com/touch-pi-portable-raspberry-pi) 3D printed case for my screen and raspberry pi, and with a battery and [PowerBoost 500c](https://www.adafruit.com/product/1944) charger it makes a great base for raspberry pi projects.

I wanted a way to do common tasks like going to the desktop, rebooting and shutting down without needing to use a keyboard.  I also wanted the screen to display the current IP address to make it easier to ssh into the device.

Written using python and pygame the 3.5" screen is broken out into 8 large touchable menu areas.

## Installation

    git clone https://github.com/garthvh/pitftmenu
    cd pitftmenu

### 8 Button Menu Template

The basic 8 Button Template can be run with the following command the buttons in this example simply print out the number of the button pushed and closes the menu:

![8 Button Menu Template](http://garthvh.com/assets/img/touchpi/menu_8button.jpg "8 Button Menu Template")

    sudo python menu_8button.py

### Generic Touch Pi Menu

My basic touch pi menu with a top label with your hostname and IP address, one open button and working buttons for Desktop, Terminal, Configuring Wifi, Reboot and Shutdown.

WiFi Functionality Requires PiFi and Virtual Keyboard.

![Touch Pi Menu](http://garthvh.com/assets/img/touchpi/menu_touchpi.jpg "Touch Pi Menu")

![Touch Pi Menu 2](http://garthvh.com/assets/img/touchpi/menu_touchpi_2.jpg "Touch Pi Menu2")

    sudo python menu_touchpi.py

### Reboot and Shutdown Buttons

If you want to enable the reboot and shutdown commands you will need to make the following updates

    sudo visudo

Add the following lines to the end of the file to target the www-data user

    www-data ALL=/sbin/shutdown
    www-data ALL=NOPASSWD: /sbin/shutdown

### Automatic low battery shutdown

I have connected the LBO pin on the PowerBoost 500c to GPIO Pin 21, when it returns low the TouchPi shuts down.

![Touch Pi Menu 2](http://garthvh.com/assets/img/touchpi/menu_touchpi_3.jpg "Touch Pi Menu2")

### Run menu at startup

If you want the script to run at startup, add a cron job

    sudo crontab -e

And add the following line to the bottom of the file

    @reboot python /home/pi/pitftmenu/menu_touchpi.py &

## References

The examples here are cobbled together from other code linked to below:

- https://github.com/5Volt-Junkie/RPi-Tron-Radio/blob/master/tron-radio.py
- http://richardhawthorn.com/?p=128
- http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/
- https://github.com/DoctorBud/raspberrypi-node/tree/176f7536d505de17b0d790855a836e0d2cb7d059/pitft-pygame
- https://learn.adafruit.com/pi-video-output-using-pygame/pygame-drawing-functions
- https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
- http://home.uktechreviews.com/Raspberry/Pi%20blog/files/pygame-menu.html
