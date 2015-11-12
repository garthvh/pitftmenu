#!/bin/bash
echo Starting X
sudo -u pi FRAMEBUFFER=/dev/fb1 startx
python /home/pi/pitftmenu/menu_kali-1.py &
