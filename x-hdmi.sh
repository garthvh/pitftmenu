#!/bin/bash
echo Starting X
sudo -u pi FRAMEBUFFER=/dev/fb0 startx
python /home/pi/pitftmenu/menu_kali-1.py &
