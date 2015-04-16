import sys, pygame, socket
from pygame.locals import *
import time
import subprocess
import os
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()

#define function for printing text in a specific place and with a specific colour and adding a border
def make_button(text, xpo, ypo, height, width, colour):
    font=pygame.font.Font(None,42)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, cyan, (xpo-10,ypo-10,width,height),3)

# define function that checks for touch location
def on_touch():
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

    #  x_min                 x_max   y_min                y_max
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
            button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
            button(4)
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
            button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
            button(6)

# Get Your External IP Address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

#define action on pressing buttons
def button(number):
    print "You pressed button ",number

    if number == 3:
        # desktop
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Launching Desktop now!", 1, (white))
        screen.blit(label,(50,120))
        pygame.display.flip()
        pygame.quit()
        subprocess.call("FRAMEBUFFER=/dev/fb1 startx", shell=True)
        sys.exit()

    if number == 4:
        # exit
        sys.exit()

    if number == 5:
        # reboot
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Rebooting Now!", 1, (white))
        screen.blit(label,(50,120))
        pygame.display.flip()
        restart()
        sys.exit()

    if number == 6:
        # shutdown
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Shutting Down Now!", 1, (white))
        screen.blit(label,(50,120))
        pygame.display.flip()
        shutdown()
        pygame.quit()
        sys.exit()


#set size of the screen
size = width, height = 480, 320

#colors     R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)

screen = pygame.display.set_mode(size)

#set up the fixed items on the menu
screen.fill(black) #change the colours if needed
pygame.draw.rect(screen, cyan, (0,0,480,320),10)

#Add buttons and labels
# First Row Label
make_button("  Garth's Simple Pi Interface ", 30, 30, 55, 440, cyan)
# Second Row buttons 3 and 4
make_button(" Desktop ", 30, 105, 55, 210, cyan)
make_button("     Exit", 260, 105, 55, 210, cyan)
# Third Row buttons 5 and 6
make_button("    Reboot    ", 40, 180, 50, 200, cyan)
make_button("   Shutdown ", 260, 180, 50, 200, cyan)
# Fourth Row Label
make_button("    Current IP: " +  get_ip(), 40, 250, 50, 420, cyan)

#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print "screen pressed" #for debugging purposes
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print pos #for checking
            pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
            on_touch()

#ensure there is always a safe way to end the program if the touch screen fails

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
