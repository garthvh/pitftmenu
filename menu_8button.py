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
    pygame.draw.rect(screen, blue, (xpo-10,ypo-10,width,height),3)

#define function that checks for mouse location
def on_click():
    click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    # click_pos[0] = x
    # click_pos[1] = y

    # button 1 event
    if 30 <= click_pos[0] <= 240 and 30 <= click_pos[1] <=80:
            print "You pressed button 1 in column 1"
            button(1)
    # button 2 event
    if 260 <= click_pos[0] <= 460 and 40 <= click_pos[1] <=90:
            print "You pressed button 1 in column 2"
            button(2)
    # button 3 event
    if 40 <= click_pos[0] <= 240 and 100 <= click_pos[1] <=150:
            print "You pressed button 2 in column 1 (button 3)"
            button(3)
    # button 4 event
    if 260 <= click_pos[0] <= 460 and 100 <= click_pos[1] <=150:
            print "You pressed button 2 in column 2"
            button(4)
    # button 5 event
    if 40 <= click_pos[0] <= 240 and 160 <= click_pos[1] <=210:
            print "You pressed button 3 in column 1"
            button(5)
    # button 6 event
    if 260 <= click_pos[0] <= 460 and 160 <= click_pos[1] <=210:
            print "You pressed button 3 in column 2"
            button(6)
    #now check to see if button 7 was pressed
    if 40 <= click_pos[0] <= 240 and 240 <= click_pos[1] <=290:
            print "You pressed button 4 in column 1"
            button(7)
    #now check to see if button 8 was pressed
    if 260 <= click_pos[0] <= 460 and 240 <= click_pos[1] <=290:
            print "You pressed the button 4 in column 2"
            button(8)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

#run Commands
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

#define action on pressing buttons
def button(number):
    print "You pressed button ",number

    if number == 1:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 2:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 3:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 4:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 5:
        screen.fill(black)
        font=pygame.font.Font(None,36)
        label=font.render("Good Bye!", 1, (white))
        screen.blit(label,(105,120))
        pygame.display.flip()
        time.sleep(5)
        sys.exit()

    if number == 6:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 7:
        time.sleep(5) #do something interesting here
        sys.exit()

    if number == 8:
        time.sleep(5) #do something interesting here
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
cream   = (254, 255, 250)

screen = pygame.display.set_mode(size)
"""
Set up the base menu you can customize your menu with the colors above
"""
# Background Color
screen.fill(black)

# Outer Border
pygame.draw.rect(screen, blue, (0,0,480,320),10)

# Buttons and labels
# First Row
make_button("Menu Item 1", 30, 30, 55, 210, blue)
make_button("Menu Item 2", 260, 30, 55, 210, blue)
# Second Row
make_button("Menu Item 3", 40, 110, 50, 200, blue)
make_button("Menu item 4", 260, 110, 50, 200, blue)
# Third Row
make_button("Menu item 5", 40, 180, 50, 200, blue)
make_button("Menu item 6", 260, 180, 50, 200, blue)
# Fourth Row
make_button("Menu item 7", 30, 260, 55, 210, blue)
make_button("Menu item 8", 260, 260, 55, 210, blue)

#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print "screen pressed" #for debugging purposes
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            print pos #for checking
            pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
            on_click()

#ensure there is always a safe way to end the program if the touch screen fails

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
