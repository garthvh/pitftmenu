#!/usr/bin/env python
import pygame, os, subprocess, time
from pygame.locals import *
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
pygame.font.init()
pygame.display.init()
pygame.mouse.set_visible(0)

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

# Turn screen on
def screen_on():
        pygame.quit()
	run_cmd("/usr/bin/gpio -g mode 18 pwm")
	run_cmd("/usr/bin/gpio pwmc 1000")
	run_cmd("/usr/bin/gpio -g pwm 18 1023")
        page=os.environ["MENUDIR"] + "menu_kali-1.py"
        os.execvp("python", ["python", page])
        os.execvp("python", ["python", "menu_kali-1.py"])


# Turn screen off
run_cmd("/usr/bin/gpio -g mode 18 pwm")
run_cmd("/usr/bin/gpio pwmc 1000")
run_cmd("/usr/bin/gpio -g pwm 18 0")


#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            screen_on()

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    time.sleep(0.4)
