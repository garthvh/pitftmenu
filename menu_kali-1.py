import sys, pygame, socket
from pygame.locals import *
import time
import subprocess
import os
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame and hide mouse
pygame.init()
pygame.mouse.set_visible(0)

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    font=pygame.font.Font(None,42)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, green, (xpo-10,ypo-10,width,height),5)

# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
            button(1)
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
            button(2)
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
            button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
            button(4)
##    # button 5 event
##    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
##            button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
            button(6)

def get_temp():
    command = "vcgencmd measure_temp"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

# Define each button press action
def button(number):
    print "You pressed button ",number

    if number == 1:
        # X TFT
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Launching X on TFT Display", 1, (white))
        screen.blit(label,(10,120))
        pygame.display.flip()
        pygame.quit()
        subprocess.call("FRAMEBUFFER=/dev/fb1 startx", shell=True)
        #run_cmd("FRAMEBUFFER=/dev/fb1 startx")
        sys.exit()

    if number == 2:
        # X HDMI
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Launching X on HDMI Display", 1, (white))
        screen.blit(label,(10,120))
        pygame.display.flip()
        pygame.quit()
        subprocess.call("FRAMEBUFFER=/dev/fb0 startx", shell=True)
        #run_cmd("FRAMEBUFFER=/dev/fb0 startx")
        sys.exit()

    if number == 3:
        # exit
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("Exiting to Terminal", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        sys.exit()

    if number == 4:
        # SDR-Scanner
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("SDR-Scanner. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        os.system("python /home/pi/FreqShow/freqshow.py")
        sys.exit()


    if number == 6:
        # next page
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Next Page. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        os.system("python /home/pi/pitftmenu/menu_kali-2.py")
        sys.exit()



# colors    R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 480, 320
screen = pygame.display.set_mode(size)

# Background Color
screen.fill(black)

# Outer Border
pygame.draw.rect(screen, green, (0,0,480,320),10)
pi_hostname = run_cmd("hostname")
pi_hostname = "  " + pi_hostname[:-1]
# Buttons and labels
# First Row Label
make_label(pi_hostname, 32, 30, 48, green)
# Second Row buttons 3 and 4
make_button("   X on TFT", 30, 105, 55, 210, green)
make_button("   X on HDMI", 260, 105, 55, 210, green)
# Third Row buttons 5 and 6
make_button("   Terminal", 30, 180, 55, 210, green)
make_button(" SDR-Scanner", 260, 180, 55, 210, green)
# Fourth Row Buttons
## make_button(" ", 30, 255, 55, 210, green)
make_button("         >>>", 260, 255, 55, 210, green)


#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            on_touch()

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
