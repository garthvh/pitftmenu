# Simple PiTFT TouchPi Menu System

Simple touch menu for Raspberry Pi projects using the [3.5" Adafruit PiTFT](http://www.adafruit.com/products/2097) 480x320 touch screen.

Runs as a python script in the framebuffer without needing a desktop environment.

Featured on the adafruit blog for pi day:
<blockquote class="twitter-tweet" lang="en">
	<p lang="ht" dir="ltr">Simple PiTFT TouchPi Menu System <a href="https://twitter.com/hashtag/piday?src=hash">#piday</a> <a href="https://twitter.com/hashtag/raspberrypi?src=hash">#raspberrypi</a> <a href="https://twitter.com/Raspberry_Pi">@Raspberry_Pi</a> <a href="http://t.co/JT9CbFiwvz">http://t.co/JT9CbFiwvz</a></p>&mdash; adafruit industries (@adafruit) <a href="https://twitter.com/adafruit/status/596675973615071232">May 8, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I have made a model b+ [Touch Pi](https://learn.adafruit.com/touch-pi-portable-raspberry-pi) 3D printed case for my screen and raspberry pi, and with a battery and [PowerBoost 500c](https://www.adafruit.com/product/1944) charger it makes a great base for raspberry pi projects.

I wanted a way to do common tasks like going to the desktop, rebooting and shutting down without needing to use a keyboard.  I also wanted the screen to display the current IP address to make it easier to ssh into the device.

Written using python and pygame the 3.5" screen is broken out into 8 large touchable menu areas but can be endlessly customized.

@Re4son customized the script to run the menu's on his Kali Linux penetration testing drone [Sticky Finger's Kali Pi](http://www.whitedome.com.au/kali-pi)
![Kali-Pi in action](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/2015.11-Kali-Pi-Drone_small2.jpg)


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

# [KALI-PI Launcher](http://whitedome.com.au/re4son/index.php/2015/11/16/sticky-fingers-kali-pi/) by @Re4son 

## Penetration Testing Drone Menus

This menu is the default launcher in [Sticky Finger's Kali Pi](http://www.whitedome.com.au/kali-pi)
![Kali-Pi in action](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/2015.11-Kali-Pi-Drone_small2.jpg)

I was after an easy way to launch X Window on either the TFT screen or through HDMI without the need for massive reconfigurations.
I came accross this repository and used it as basis for this project


## Installation

    git clone https://github.com/garthvh/pitftmenu
    cd pitftmenu
    customise the file "menu" to match the path
    customise the scripts to suit your needs
    
**Important: Pygame is broken on on Debian Jessie. I'll explain below how to fix it.**

## Usage
	sudo ./menu
    
## Layout

### Start Screen

The first menu is menu_kali-1.py, which provides the following options:

![menu_kali-1](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/kali-pi_01-menu_kali-1.png)

All functions are self explainatory.
After exiting and application, the screen returns back to the last menu.

The "Screen Off" function launches the python script "menu_screenoff.py", which uses the RPi.GPIO module to turn the screen off.
You can turn it back on by pressing anywhere on the screen.

Using the ">>>" button, we can scroll to the next screen, namely "menu_kali-2.py"

### menu_kali-2.py

Some more applications to launch:

![menu_kali-2.py](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/kali-pi_03-menu_kali-2.png)

Kismet and SDR-Scanner have to be installed for this to work.
If you want to enable the reboot and shutdown commands you will need to make the following updates

    sudo visudo
Add the following line:

    %pi	ALL=(ALL:ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown, /home/pi/pitftmenu/menu

### menu_kali-3.py

This script allows us to stop and start services:

![menu_kali-3.py](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/kali-pi_06-menu_kali-3.png)
Press a button to start a service.

The button changes to green when the service is running:

![running service](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/kali-pi_09-services-on.png)
Press the button again to stop the service.

### menu_kali-3.py
The last script displays some health information:

![menu_kali-9](http://whitedome.com.au/re4son/wp-content/uploads/2015/11/kali-pi_10-menu_kali-9.png)

### Run menu at startup

The preferred method to run this script on startup is to add it to the end of ".profile"

    nano ~/home/.profile

And add the following line to the bottom of the file

    sudo /home/pi/pitftmenu/menu
    
## Fix Pygame on Debian Jessie
The package "libsdl1.2-15-10", which ships with Debian Jessie, breaks pygame.
To make it work we have to revert back to "libsdl1.2-15-5" from Wheezy.

The quickest way is to comment everything out in your /etc/apt/sources.list and temporarily add:

```
deb http://archive.raspbian.org/raspbian wheezy main contrib non-free
```


Import the corresponding keys:
```
deb http://archive.raspbian.org/raspbian wheezy main contrib non-free
gpg -a --export 9165938D90FDDD2E | sudo apt-key add -
```

Remove the offending package and replace it with the working one:
```
sudo apt-get update
sudo apt-get remove libsdl1.2debian python-pygame
apt-get install libsdl-image1.2 libsdl-mixer1.2 libsdl-ttf2.0-0 libsdl1.2debian libsmpeg0 python-pygame
sudo apt-mark hold libsdl1.2debian
```

Restore "/etc/apt/sources.list" to it's original state.

That's it. Pygame is fixed :-)

## References

The examples here are cobbled together from other code linked to below:

- https://github.com/5Volt-Junkie/RPi-Tron-Radio/blob/master/tron-radio.py
- http://richardhawthorn.com/?p=128
- http://www.raspberrypi-spy.co.uk/2013/07/running-a-python-script-at-boot-using-cron/
- https://github.com/DoctorBud/raspberrypi-node/tree/176f7536d505de17b0d790855a836e0d2cb7d059/pitft-pygame
- https://learn.adafruit.com/pi-video-output-using-pygame/pygame-drawing-functions
- https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
- http://home.uktechreviews.com/Raspberry/Pi%20blog/files/pygame-menu.html
- http://whitedome.com.au/re4son/index.php/2015/11/16/sticky-fingers-kali-pi/
