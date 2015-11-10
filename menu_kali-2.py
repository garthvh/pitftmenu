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
##    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
##            button(3)
    # button 4 event
##    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
##            button(4)
    # button 5 event
##    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
##            button(5)
    # button 6 event
##    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
##            button(6)

# Get Your External IP Address
def get_ip():
    ip_msg = "Not connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_msg=" IP: " + s.getsockname()[0]
    except Exception:
        pass
    return ip_msg

# Restart Raspberry Pi
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

# Shutdown Raspberry Pi
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

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
        # shutdown
         screen.fill(black)
         font=pygame.font.Font(None,72)
         label=font.render("Shutting Down. .", 1, (white))
         screen.blit(label,(40,120))
         pygame.display.flip()
         pygame.quit()
         shutdown()
         sys.exit()

    if number == 2:
        # reboot
         screen.fill(black)
         font=pygame.font.Font(None,72)
         label=font.render("Rebooting. .", 1, (white))
         screen.blit(label,(40,120))
         pygame.display.flip()
         pygame.quit()
         restart()
         sys.exit()

    if number == 5:
        # Previous page
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Previous Page. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        os.system("python /home/pi/pitftmenu/menu_kali-1.py")
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
# Buttons and labels
# First Row Label
make_label(get_ip(), 32, 30, 48, green)
# Second Row buttons 1 and 2
make_button("    Shutdown", 30, 105, 55, 210, green)
make_button("      Reboot", 260, 105, 55, 210, green)
# Third Row buttons 3 and 4
## make_button("  ", 30, 180, 55, 210, green)
## make_button("  ", 260, 180, 55, 210, green)
# Fourth Row Buttons
make_button("  <<<", 30, 255, 55, 210, green)
## make_button("  ", 260, 255, 55, 210, green)


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
