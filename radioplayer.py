import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()


#define function that checks for mouse location
def on_click():
	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#check to see if exit has been pressed
	if 270 <= click_pos[0] <= 320 and 10 <= click_pos[1] <=50:
		print "You pressed exit"
		button(0)
	#now check to see if play was pressed
	if 20 <= click_pos[0] <= 70 and 80 <= click_pos[1] <=130:
                print "You pressed button play"
                button(1)
	#now check to see if stop  was pressed
        if 80 <= click_pos[0] <= 135 and 80 <= click_pos[1] <=130:
                print "You pressed button stop"
                button(2)
	#now check to see if refreshed  was pressed
        if 270 <= click_pos[0] <= 320 and 70 <= click_pos[1] <=120:
                print "You pressed button refresh"
                button(3)
	#now check to see if previous  was pressed
        if 10 <= click_pos[0] <= 60 and 180 <= click_pos[1] <=230:
                print "You pressed button previous"
                button(4)

	 #now check to see if next  was pressed
        if 70 <= click_pos[0] <= 120 and 180 <= click_pos[1] <=230:
                print "You pressed button next"
                button(5)

	 #now check to see if volume down was pressed
        if 130 <= click_pos[0] <= 180 and 180 <= click_pos[1] <=230:
                print "You pressed volume down"
                button(6)

	 #now check to see if button 7 was pressed
        if 190 <= click_pos[0] <= 240 and 180 <= click_pos[1] <=230:
                print "You pressed volume up"
                button(7)

	 #now check to see if button 8 was pressed
        if 250 <= click_pos[0] <= 300 and 180 <= click_pos[1] <=230:
                print "You pressed mute"
                button(8)

	 #now check to see if button 9 was pressed
        if 15 <= click_pos[0] <= 125 and 165 <= click_pos[1] <=200:
                print "You pressed button 9"
                button(9)


#define action on pressing buttons
def button(number):
	print "You pressed button ",number
	if number == 0:    #specific script when exiting
		screen.fill(black)
		font=pygame.font.Font(None,24)
        	label=font.render("Radioplayer will continue in background", 1, (white))
        	screen.blit(label,(0,90))
		pygame.display.flip()
		time.sleep(5)
		sys.exit()

	if number == 1:
		subprocess.call("mpc play ", shell=True)
		refresh_menu_screen()

	if number == 2:
		subprocess.call("mpc stop ", shell=True)
		refresh_menu_screen()

	if number == 3:
		subprocess.call("mpc stop ", shell=True)
		subprocess.call("mpc play ", shell=True)
		refresh_menu_screen()

	if number == 4:
		subprocess.call("mpc prev ", shell=True)
		refresh_menu_screen()

	if number == 5:
		subprocess.call("mpc next ", shell=True)
		refresh_menu_screen()

	if number == 6:
		subprocess.call("mpc volume -10 ", shell=True)
		refresh_menu_screen()

	if number == 7:
		subprocess.call("mpc volume +10 ", shell=True)
		refresh_menu_screen()

	if number == 8:
		subprocess.call("mpc volume 0 ", shell=True)
		refresh_menu_screen()

def refresh_menu_screen():
#set up the fixed items on the menu
	screen.fill(white) #change the colours if needed
	font=pygame.font.Font(None,24)
	title_font=pygame.font.Font(None,34)
	station_font=pygame.font.Font(None,20)
	label=title_font.render("MPC RADIO", 1, (blue))
	label2=font.render("Streaming Internet Radio", 1, (red))
	screen.blit(label,(105, 15))
	screen.blit(label2,(88, 45))
	play=pygame.image.load("play.tiff")
	pause=pygame.image.load("pause.tiff")
	refresh=pygame.image.load("refresh.tiff")
	previous=pygame.image.load("previous.tiff")
	next=pygame.image.load("next.tiff")
	vol_down=pygame.image.load("volume_down.tiff")
	vol_up=pygame.image.load("volume_up.tiff")
	mute=pygame.image.load("mute.png")
	exit=pygame.image.load("exit.tiff")
	radio=pygame.image.load("radio.tiff")
	# draw the main elements on the screen
	screen.blit(play,(20,80))
	screen.blit(pause,(80,80))
	pygame.draw.rect(screen, red, (8, 70, 304, 108),1)
	pygame.draw.line(screen, red, (8,142),(310,142),1)
	pygame.draw.rect(screen, cream, (10, 143, 300, 33),0)
	screen.blit(refresh,(270,70))
	screen.blit(previous,(10,180))
	screen.blit(next,(70,180))
        screen.blit(vol_down,(130,180))
	screen.blit(vol_up,(190,180))
	screen.blit(mute,(250,180))
        screen.blit(exit,(270,5))
	screen.blit(radio,(2,1))
	pygame.draw.rect(screen, blue, (0,0,320,240),3)
	##### display the station name and split it into 2 parts :
	station = subprocess.check_output("mpc current", shell=True )
	lines=station.split(":")
	length = len(lines)
	if length==1:
		line1 = lines[0]
		line1 = line1[:-1]
		line2 = "No additional info: "
	else:
		line1 = lines[0]
		line2 = lines[1]

	line2 = line2[:42]
	line2 = line2[:-1]
	#trap no station data
	if line1 =="":
		line2 = "Press PLAY or REFRESH"
		station_status = "stopped"
		status_font = red
	else:
		station_status = "playing"
		status_font = green
	station_name=station_font.render(line1, 1, (red))
	additional_data=station_font.render(line2, 1, (blue))
	station_label=title_font.render(station_status, 1, (status_font))
	screen.blit(station_label,(175,100))
	screen.blit(station_name,(13,145))
	screen.blit(additional_data,(12,160))
	######## add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:]
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (black))
	screen.blit(volume_tag,(175,75))
	####### check to see if the Radio is connected to the internet
	IP = subprocess.check_output("hostname -I", shell=True )
	IP=IP[:3]
	if IP =="192":
		network_status = "online"
		status_font = green

	else:
		network_status = "offline"
		status_font = red

	network_status_label = font.render(network_status, 1, (status_font))
	screen.blit(network_status_label, (215,75))
	pygame.display.flip()

def main():
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
        time.sleep(0.2)
	pygame.display.update()


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
size = width, height = 480, 320
screen = pygame.display.set_mode(size)

#define colours
blue = 26, 0, 255
cream = 254, 255, 25
black = 0, 0, 0
white = 255, 255, 255
yellow = 255, 255, 0
red = 255, 0, 0
green = 0, 255, 0
refresh_menu_screen()  #refresh the menu interface
main() #check for key presses and start emergency exit
station_name()
