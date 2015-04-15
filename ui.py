# -*- coding: utf-8 -*-
import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
import re
import pylast
from mpd import MPDClient
from math import ceil
import datetime
from datetime import timedelta
import pitft_ui
from signal import alarm, signal, SIGALRM, SIGTERM, SIGKILL
import logging
from logging.handlers import TimedRotatingFileHandler
from daemon import Daemon

# OS enviroment variables for pitft
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Logging configs
logger = logging.getLogger("PMB PiTFT logger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler('pmb-pitft.log',when="midnight",interval=1,backupCount=14)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

## HAX FOR FREEZING ##
class Alarm(Exception):
	pass
def alarm_handler(signum, frame):
	logger.debug("ALARM")
	raise Alarm
## HAX END ##

def signal_term_handler(signal, frame):
    logger.debug('got SIGTERM')
    sys.exit(0)

class PMBPitftDaemon(Daemon):
	sm = None
	client = None
	network = None
	screen = None

	# Setup Python game, MPD, Last.fm and Screen manager
	def setup(self):
		logger.info("Starting setup")
		signal(SIGTERM, signal_term_handler)
		# Python game ######################
		logger.info("Setting pygame")
		pygame.init()
		pygame.mouse.set_visible(False)

		# Hax for freezing
		signal(SIGALRM, alarm_handler)
		alarm(3)
		try:
			# Set screen size
			size = width, height = 320, 240
			self.screen = pygame.display.set_mode(size)
			alarm(0)
		except Alarm:
			logger.debug("Keyboard interrupt?")
			raise KeyboardInterrupt
		# Hax end

		logger.info("Display driver: %s" % pygame.display.get_driver())

		# MPD ##############################
		logger.info("Setting MPDClient")
		self.client = MPDClient()
		self.client.timeout = 10
		self.client.idletimeout = None

		# Pylast ####################################################################  
		logger.info("Setting Pylast")
		# You have to have your own unique two values for API_KEY and API_SECRET
		# Obtain yours from http://www.last.fm/api/account for Last.fm
		API_KEY = "dcbf56084b47ffbd3cc6755724cb12fa"
		API_SECRET = "a970660ef47453134192fa6a9fa6da31"

		# In order to perform a write operation you need to authenticate yourself
		#username = "your_user_name"
		#password_hash = pylast.md5("your_password")
		self.network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

		# Screen manager ###############
		logger.info("Setting screen manager")
		try:
			self.sm = pitft_ui.PmbPitft(self.client, self.network, logger)
		except Exception, e:
			logger.exception(e)
			raise

	# Connect to MPD server
	def connectToMPD(self):
		logger.info("Trying to connect MPD server")
		noConnection = True
		while noConnection:
			try:
				self.client.connect("localhost", 6600)
				noConnection=False
			except Exception, e:
				logger.info(e)
				noConnection=True
				time.sleep(15)
		logger.info("Connection to MPD server established.")

	# Click handler
	def on_click(self):
		click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

		# Screen is off and its touched
		if self.sm.get_backlight_status() == 0 and 0 <= click_pos[0] <= 320 and 0 <= click_pos[1] <= 240:
			logger.debug("Screen off, Screen touch")
			self.button(9)
		# Screen is on. Check which button is touched 
		else:
			# There is no multi touch so if one button is pressed another one can't be pressed at the same time
			if 280 <= click_pos[0] <= 320 and 200 <= click_pos[1] <=240:
				logger.debug("Screen off")
				button(9)
			elif 223 <= click_pos[0] <= 285 and 6 <= click_pos[1] <=31:
				logger.debug("Toggle repeat") 
				self.button(0)
			elif 223 <= click_pos[0] <= 285 and 38 <= click_pos[1] <=63:
				logger.debug("Toggle random")
				self.button(1)	
			# Volume
			elif 188 <= click_pos[0] <= 226 and 65 <= click_pos[1] <=100:
					logger.debug("Volume-")
					self.button(2)
			elif 281 <= click_pos[0] <= 319 and 65 <= click_pos[1] <=100:
					logger.debug("Volume+")
					self.button(3)
			# SLEEP
			elif 188 <= click_pos[0] <= 226 and 103 <= click_pos[1] <=138:
					logger.debug("Sleep-")
					self.button(4)
			elif 281 <= click_pos[0] <= 319 and 103 <= click_pos[1] <=138:
					logger.debug("Sleep+")
					self.button(5)
			# Controls
			elif 194 <= click_pos[0] <= 232 and 144 <= click_pos[1] <=182:
					logger.debug("Prev")
					self.button(6)
			elif 234 <= click_pos[0] <= 272 and 144 <= click_pos[1] <=182:
					logger.debug("Toggle play/pause")
					self.button(7)
			elif 273 <= click_pos[0] <= 311 and 144 <= click_pos[1] <=182:
					logger.debug("Next")
					self.button(8) 

	#define action on pressing buttons
	def button(self, number):
		logger.debug("You pressed button %s" % number)
		if number == 0:    #specific script when exiting
			self.sm.toggle_repeat()

		elif number == 1:	
			self.sm.toggle_random()

		elif number == 2:
			self.sm.set_volume(1, "-")

		elif number == 3:
			self.sm.set_volume(1, "+")
			
		elif number == 4:
			self.sm.adjust_sleeptimer(15, "-")

		elif number == 5:
			self.sm.adjust_sleeptimer(15, "+")

		elif number == 6:
			self.sm.control_player("previous")

		elif number == 7:
			self.sm.toggle_playback()

		elif number == 8:
			self.sm.control_player("next")

		elif number == 9:
			self.sm.toggle_backlight()
	
	def shutdown(self):
		# Close MPD connection
		if self.client:
			self.client.close()
			self.client.disconnect()

	# Main loop
	def run(self):
		self.setup()
		self.connectToMPD()
		try:
			drawtime = datetime.datetime.now()
			while 1:
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						logger.debug("screen pressed") #for debugging purposes
						pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
						logger.debug(pos[0])
						#pygame.draw.circle(screen, (255,255,255), pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
						self.on_click()
						

				# Update screen
				if drawtime < datetime.datetime.now():
					drawtime = datetime.datetime.now() + timedelta(milliseconds=500)
					self.sm.refresh_mpd()
					self.sm.parse_mpd()
					self.sm.render(self.screen)
					pygame.display.flip()
			pygame.display.update()
		except Exception, e:
			logger.debug(e)
			raise

if __name__ == "__main__":
	daemon = PMBPitftDaemon('/tmp/pmbpitft-daemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.shutdown()
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)