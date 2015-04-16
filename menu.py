import sys, pygame
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
def make_button(text, xpo, ypo, colour):
    font=pygame.font.Font(None,42)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, cyan, (xpo-10,ypo-10,200,50),1)

#define function that checks for mouse location
def on_click():
    click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    # click_pos[0] = x
    # click_pos[1] = y
    #now check to see if button 1 was pressed
    if 40 <= click_pos[0] <= 240 and 40 <= click_pos[1] <=90:
            print "You pressed button 1 in column 1"
            button(1)
    #now check to see if button 2 was pressed
    if 260 <= click_pos[0] <= 460 and 40 <= click_pos[1] <=90:
            print "You pressed button 1 in column 2"
            button(2)
    #now check to see if button 3 was pressed
    if 40 <= click_pos[0] <= 240 and 100 <= click_pos[1] <=150:
            print "You pressed button 2 in column 1"
            button(3)
    #now check to see if button 4 was pressed
    if 260 <= click_pos[0] <= 460 and 100 <= click_pos[1] <=150:
            print "You pressed button 2 in column 2"
            button(4)
    #now check to see if button 5 was pressed
    if 40 <= click_pos[0] <= 240 and 160 <= click_pos[1] <=210:
            print "You pressed button 3 in column 1"
            button(5)
    #now check to see if button 6 was pressed
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

#run Commands
def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

#define action on pressing buttons
def button(number):
    print "You pressed button ",number
    if number == 0:    #specific script when exiting
        screen.fill(black)
        font=pygame.font.Font(None,36)
        label=font.render("Good Bye!", 1, (white))
        screen.blit(label,(105,120))
        pygame.display.flip()
        time.sleep(5)
        sys.exit()

    if number == 1:
        screen.fill(black)
        font=pygame.font.Font(None,36)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        label=font.render(s.connect(('google.com', 0)), 1, (white))
        screen.blit(label,(105,120))
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
        time.sleep(5) #do something interesting here
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

#set up the fixed items on the menu
screen.fill(black) #change the colours if needed
#logo=pygame.image.load("logo.tiff")
#exit=pygame.image.load("exit.tiff")
#screen.blit(logo,(210,5))
#screen.blit(exit,(200,130))
pygame.draw.rect(screen, cyan, (0,0,480,320),10)

#Add buttons and labels
# First Row
make_button("Menu item 1", 40, 40, cyan)
make_button("Menu item 2", 260, 40, cyan)
# Second Row
make_button("Menu item 3", 40, 110, cyan)
make_button("Menu item 4", 260, 110, cyan)
# Third Row
make_button("Menu item 5", 40, 180, cyan)
make_button("Menu item 6", 260, 180, cyan)
# Fourth Row
make_button("Menu item 7", 40, 250, cyan)
make_button("Menu item 8", 260, 250, cyan)

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
