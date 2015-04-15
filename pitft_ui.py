# -*- coding: utf-8 -*-
import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
import re
from math import ceil
from threading import Thread
from mpd import MPDClient

import datetime
from datetime import timedelta

class PmbPitft:
	def __init__(self, client, lfm, logger):
		self.mpdc = client
		self.lfm = lfm
		self.logger = logger

		# Paths
		self.path = os.path.dirname(sys.argv[0]) + "/"
		os.chdir(self.path)
		
		# Fonts
		self.fontfile = self.path + "helvetica-neue-bold.ttf"
		self.font = {}
		self.font['details']	= pygame.font.Font(self.fontfile, 10)
		self.font['field']		= pygame.font.Font(self.fontfile, 16)

		# Images
		self.image = {}
		self.image["background"]			=pygame.image.load(self.path + "background.png")
		self.image["coverart_place"]		=pygame.image.load(self.path + "coverart-placer.png")
		self.image["details"]				=pygame.image.load(self.path + "details.png")
		self.image["field"]					=pygame.image.load(self.path + "field-value.png")
		self.image["indicator_blue"]		=pygame.image.load(self.path + "indicator-blue.png")
		self.image["indicator_red"]			=pygame.image.load(self.path + "indicator-red.png")
		self.image["position_bg"]			=pygame.image.load(self.path + "position-background.png")
		self.image["position_fg"]			=pygame.image.load(self.path + "position-foreground.png")
		self.image["icon_randomandrepeat"]	=pygame.image.load(self.path + "randomandrepeat.png")
		self.image["icon_screenoff"]		=pygame.image.load(self.path + "screen-off.png")
	
		## Buttons
		self.image["button_next"]		=pygame.image.load(self.path + "button-next.png")
		self.image["button_pause"]		=pygame.image.load(self.path + "button-pause.png")
		self.image["button_play"]		=pygame.image.load(self.path + "button-play.png")
		self.image["button_prev"]		=pygame.image.load(self.path + "button-prev.png")
		self.image["button_timeminus"]	=pygame.image.load(self.path + "button-timeminus.png")
		self.image["button_timeplus"]	=pygame.image.load(self.path + "button-timeplus.png")
		self.image["button_volumeminus"]=pygame.image.load(self.path + "button-volumeminus.png")
		self.image["button_volumeplus"]	=pygame.image.load(self.path + "button-volumeplus.png")
		self.image["button_toggle_off"]	=pygame.image.load(self.path + "toggle-off.png")
		self.image["button_toggle_on"]	=pygame.image.load(self.path + "toggle-on.png")
		self.image["nocover"]			=pygame.image.load(self.path + "no-cover.png")
		
		# Threads
		self.coverartThread = None
		self.oldCoverartThreadRunning = False

		# Things to remember
		self.sleepTimer = None
		self.processingCover = False
		self.coverFetched = False
		self.status = {}
		self.song = {}
		self.reconnect = False

		# Things to show
		self.trackfile = None
		self.artist = "NONE"
		self.album = "NONE"
		self.title = "NONE"
		self.timeElapsed = "00:00"
		self.timeTotal = "00:00"
		self.timeElapsedPercentage = 0
		self.playbackStatus = "stop"
		self.sleepTimerText = "OFF"
		self.volume = 0
		self.random = 0
		self.repeat = 0
		self.cover = False

		# What to update
		self.updateTrackInfo = False
		self.updateAlbum	 = False	
		self.updateElapsed	 = False
		self.updateRandom	 = False
		self.updateRepeat	 = False
		self.updateVolume	 = False
		self.updateState	 = False
		self.updateSleepTimer= False
		self.updateAll		 = True

		# Print data
		self.logger.info("MPD server version: %s" % self.mpdc.mpd_version)
		
		# Turn backlight on
		self.turn_backlight_on()

	def refresh_mpd(self):
		if self.reconnect:
			self.reconnect_mpd()
		if self.reconnect == False:
			connection = False
			try:
				self.status = self.mpdc.status()
				self.song = self.mpdc.currentsong()
				connection = True
			except Exception as e:
				self.logger.debug(e)
				connection = False
				self.status = {}
				self.song = {}

			if connection == False:
				try:
					if e.errno == 32:
						self.reconnect = True
					else:
						print "Nothing to do"
				except Exception, e:
					self.reconnect = True
					self.logger.debug(e)

	def reconnect_mpd(self):
		self.logger.info("Reconnecting to MPD server")
		client = MPDClient()
		client.timeout = 10
		client.idletimeout = None
		noConnection = True
		while noConnection:
			try:
				client.connect("localhost", 6600)
				noConnection=False
			except Exception, e:
				self.logger.info(e)
				noConnection=True
				time.sleep(15)
		self.mpdc = client
		self.reconnect = False
		self.logger.info("Connection to MPD server established.")


	def parse_mpd(self):
		# -------------
		# |  PARSE    |
		# -------------
		# Artist
		try:
			artist = self.song["artist"].decode('utf-8')
		except:
			artist = "NONE"
		
		# Album
		try:
			album = self.song["album"].decode('utf-8')
		except:
			album = "NONE"

		# Track Title
		try:
			title = self.song["title"].decode('utf-8')
		except:
			title = "NONE"

		# Time elapsed
		try:
			min = int(ceil(float(self.status["elapsed"])))/60
			min = min if min > 9 else "0%s" % min
			sec = int(ceil(float(self.status["elapsed"])%60))
			sec = sec if sec > 9 else "0%s" % sec
			timeElapsed = "%s:%s" % (min,sec)
		except:
			timeElapsed = "00:00"

		# Time total
		try:
			min = int(ceil(float(self.song["time"])))/60
			min = min if min > 9 else "0%s" % min
			sec = int(ceil(float(self.song["time"])%60))
			sec = sec if sec > 9 else "0%s" % sec
			timeTotal = "%s:%s" % (min,sec)
		except:
			timeTotal = "00:00"

		# Time elapsed percentage
		try:
			timeElapsedPercentage = float(self.status["elapsed"])/float(self.song["time"])
		except:
			timeElapsedPercentage = 0

		# Playback status
		try:
			playbackStatus = self.status["state"]
		except:
			playbackStatus = "stop"

		# Repeat
		try:
			repeat = int(self.status["repeat"])
		except:
			repeat = 0

		# Random
		try:
			random = int(self.status["random"])
		except:
			random = 0

		# Volume
		try:
			volume = int(self.status["volume"])
		except:
			volume = 0

		# -------------
		# |  CHANGES  |
		# -------------
		# Artist
		if self.artist != artist:
			self.artist = artist
			self.updateTrackInfo = True

		# Album
		if self.album != album or self.oldCoverartThreadRunning:
			self.logger.debug("Album if")
			self.album = album
			self.updateAlbum = True
			self.cover = False
			# Find cover art on different thread
			try:
				if self.coverartThread:
					self.logger.debug("if caT")
					if self.coverartThread.is_alive():
						self.logger.debug("caT is alive")
						self.oldCoverartThreadRunning = True
					else:
						self.logger.debug("caT not live")
						self.oldCoverartThreadRunning = False
						self.coverartThread = Thread(target=self.fetch_coverart)
						self.logger.debug("caT go")
						self.coverartThread.start()
				else:
					self.logger.debug("not caT")
					self.coverartThread = Thread(target=self.fetch_coverart)
					self.coverartThread.start()
			except Exception, e:
				self.logger.debug("Coverartthread: %s" % e)
				self.processingCover = False

		# Track Title
		if self.title != title:
			self.title = title
			self.updateTrackInfo = True

		# Time elapsed
		if self.timeElapsed != timeElapsed:
			self.timeElapsed = timeElapsed
			self.updateElapsed = True

		# Time total
		if self.timeTotal != timeTotal:
			self.timeTotal = timeTotal
			self.updateTrackInfo = True
			self.updateElapsed = True

		# Time elapsed percentage
		if self.timeElapsedPercentage != timeElapsedPercentage:
			self.timeElapsedPercentage = timeElapsedPercentage
			self.updateElapsed = True

		# Playback status
		if self.playbackStatus != playbackStatus:
			self.playbackStatus = playbackStatus
			self.updateState = True

		# Repeat
		if self.repeat != repeat:
			self.repeat = repeat
			self.updateRepeat = True

		# Random
		if self.random != random:
			self.random = random
			self.updateRandom = True

		# Volume
		if self.volume != volume:
			self.volume = volume
			self.updateVolume = True

		# Sleeptimer
		if self.sleepTimer:
			td = self.sleepTimer - datetime.datetime.now()
			if self.sleepTimer > datetime.datetime.now():
				sleepTimerText = str(int(td.total_seconds() / 60))
				if self.sleepTimerText != sleepTimerText:
					self.sleepTimerText = sleepTimerText
					self.updateSleepTimer = True
			else:

				self.sleepTimerText = "OFF"
				self.sleepTimer = None
				self.updateSleepTimer = True
				self.sleepThread = Thread(target=self.sleep)
				self.sleepThread.start()
	
	def render(self, surface):
		if self.updateAll:
			self.updateTrackInfo = True
			self.updateAlbum	 = True	
			self.updateElapsed	 = True
			self.updateRandom	 = True
			self.updateRepeat	 = True
			self.updateVolume	 = True
			self.updateState	 = True
			self.updateSleepTimer= True
			
			surface.blit(self.image["background"], (0,0))	
			surface.blit(self.image["coverart_place"],(4,4))
			surface.blit(self.image["details"], (6, 199))
			surface.blit(self.image["icon_randomandrepeat"], (197,8))
			surface.blit(self.image["position_bg"], (35, 185))
			surface.blit(self.image["button_volumeminus"], (188, 65))
			surface.blit(self.image["button_volumeplus"], (281, 65))
			surface.blit(self.image["button_timeminus"], (188, 103))
			surface.blit(self.image["button_timeplus"], (281, 103))
			surface.blit(self.image["button_prev"], (194, 144))
			surface.blit(self.image["button_next"], (273, 144))
			surface.blit(self.image["icon_screenoff"], (300, 224))

		if self.updateAlbum or self.coverFetched:
			if self.cover:
				surface.blit(self.image["cover"], (12,12))
				self.coverFetched = False
			else:
				surface.blit(self.image["nocover"], (12,12))
			
		if self.updateTrackInfo:
			if not self.updateAll:
				surface.blit(self.image["background"], (0,181), (0,181, 320,240)) # reset background
				surface.blit(self.image["details"], (6, 199))
				surface.blit(self.image["position_bg"], (35, 185))
				surface.blit(self.image["icon_screenoff"], (300, 224))	# redraw screenoff icon

			text = self.font["details"].render(self.artist, 1,(230,228,227))
			surface.blit(text, (54, 197)) # Artist
			text = self.font["details"].render(self.album, 1,(230,228,227))
			surface.blit(text, (54, 211)) # Album
			text = self.font["details"].render(self.title, 1,(230,228,227))
			surface.blit(text, (54, 225)) # Title
			text = self.font["details"].render(self.timeTotal, 1,(230,228,227))
			surface.blit(text, (289, 183)) # Track length

		if self.updateElapsed:
			if not self.updateAll or not self.updateTrackInfo:
				surface.blit(self.image["background"], (0,181), (0,181, 287,15)) # reset background
				surface.blit(self.image["position_bg"], (35, 185))
			surface.blit(self.image["position_fg"], (34, 184),(0,0,int(254*self.timeElapsedPercentage),10))
			text = self.font["details"].render(self.timeElapsed, 1,(230,228,227))
			surface.blit(text, (5, 183)) # Elapsed

		if self.updateRepeat:
			if not self.updateAll:
				surface.blit(self.image["background"], (215,0), (215,0, 105,31)) # reset background

			if self.repeat == 1:
				surface.blit(self.image["button_toggle_on"], (223,6))
				surface.blit(self.image["indicator_blue"], (292, 7))
			else:
				surface.blit(self.image["button_toggle_off"], (223,6))
				surface.blit(self.image["indicator_red"], (292, 7))

		if self.updateRandom:
			if not self.updateAll:
				surface.blit(self.image["background"], (215,33), (215,33, 105,31)) # reset background

			if self.random == 1:
				surface.blit(self.image["button_toggle_on"], (223,38))
				surface.blit(self.image["indicator_blue"], (292, 39))
			else:
				surface.blit(self.image["button_toggle_off"], (223,38))
				surface.blit(self.image["indicator_red"], (292, 39))


		if self.updateVolume:
			if not self.updateAll:
				surface.blit(self.image["field"], (229,70), (5,4, 44,23)) # Reset field value area
			else:
				surface.blit(self.image["field"], (226, 67)) # Draw field
			
			text = self.font["field"].render(str(self.volume), 1,(230,228,227))

			pos = 227 + (48 - text.get_width())/2
			surface.blit(text, (pos, 72)) # Volume

		if self.updateState:
			if not self.updateAll:
				surface.blit(self.image["background"], (230,139), (230,139, 40,43)) # reset background
			if self.playbackStatus == "play":
				surface.blit(self.image["button_pause"], (234, 144))			
			else:
				surface.blit(self.image["button_play"], (234, 144))

		if self.updateSleepTimer:
			if not self.updateAll:
				surface.blit(self.image["field"], (229,108), (5,4, 44,23)) # Reset field value area
			else:
				surface.blit(self.image["field"], (226, 105))
			text = self.font["field"].render(self.sleepTimerText, 1,(230,228,227))
			pos = 227 + (48 - text.get_width())/2
			surface.blit(text, (pos, 110))
			
		# Reset updates
		self.resetUpdates()

	def resetUpdates(self):
		self.updateTrackInfo = False
		self.updateAlbum	 = False	
		self.updateElapsed	 = False
		self.updateRandom	 = False
		self.updateRepeat	 = False
		self.updateVolume	 = False
		self.updateState	 = False
		self.updateSleepTimer= False
		self.updateAll		 = False
		
	def fetch_coverart(self):
		self.logger.debug("caT start")
		self.processingCover = True
		self.coverFetched = False
		self.cover = False
		try:
			lastfm_album = self.lfm.get_album(self.artist, self.album)
			self.logger.debug("caT album: %s" % lastfm_album)
		except Exception, e:
			self.logger.exception(e)
			raise

		if lastfm_album:
			try:
				coverart_url = lastfm_album.get_cover_image(2)
				self.logger.debug("caT curl: %s" % coverart_url)
				if coverart_url:
					self.logger.debug("caT sp start")
					subprocess.check_output("wget -q --limit-rate=40k %s -O %s/cover.png" % (coverart_url, "/tmp/"), shell=True )
					self.logger.debug("caT sp end")
					coverart=pygame.image.load("/tmp/" + "cover.png")
					self.logger.debug("caT c loaded")
					self.image["cover"] = pygame.transform.scale(coverart, (163, 163))
					self.logger.debug("caT c placed")
					self.processingCover = False
					self.coverFetched = True
					self.cover = True
			except Exception, e:
				self.logger.exception(e)
				pass
		self.processingCover = False
		self.logger.debug("caT end")

	def toggle_random(self):
		random = (self.random + 1) % 2
		self.mpdc.random(random)

	def toggle_repeat(self):
		repeat = (self.repeat + 1) % 2
		self.mpdc.repeat(repeat)

	# Direction: +, -
	def set_volume(self, amount, direction=""):
		if direction == "+":
			volume = self.volume + amount
		elif direction == "-":
			volume = self.volume - amount
		else:
			volume = amount

		volume = 100 if volume > 100 else volume
		volume = 0 if volume < 0 else volume
		self.mpdc.setvol(volume)

	def toggle_playback(self):
		status = self.playbackStatus
		if status == "play":
			self.mpdc.pause()
		else:
			self.mpdc.play()
	
	def control_player(self, command):
		if command == "next":
			self.mpdc.next()
		elif command == "previous":
			self.mpdc.previous()
		elif command == "pause":
			self.mpdc.pause()
		elif command == "stop":
			self.mpdc.stop()
		else:
			pass

	def toggle_backlight(self):
		bl = (self.backlight + 1) % 2
		if bl == 1:
			self.turn_backlight_on()
		else:
			self.turn_backlight_off()

	def turn_backlight_off(self):
		self.logger.debug("Backlight off")
		subprocess.call("echo 1 | sudo tee /sys/class/backlight/*/bl_power", shell=True)
		self.backlight = 0

	def turn_backlight_on(self):
		self.logger.debug("Backlight on")
		subprocess.call("echo 0 | sudo tee /sys/class/backlight/*/bl_power", shell=True)
		self.backlight = 1


	def get_backlight_status(self):
		return self.backlight

	def adjust_sleeptimer(self, amount, direction):
		sleeptimer = self.sleepTimer
		if direction == "+":
			if sleeptimer:
				if timedelta(minutes=120) > (sleeptimer + timedelta(minutes=amount))-datetime.datetime.now():
					sleeptimer = sleeptimer + timedelta(minutes=amount)
				else:
					sleeptimer = datetime.datetime.now() + timedelta(minutes=120)
			else:
				sleeptimer = datetime.datetime.now() + timedelta(minutes=amount)
		else:
			if sleeptimer:
				sleeptimer = sleeptimer - timedelta(minutes=amount)
				if sleeptimer < datetime.datetime.now():
					sleeptimer = None
		self.sleepTimer = sleeptimer

	def sleep(self):
		self.logger.info("SLEEP")
		self.turn_backlight_off()
		self.control_player("stop")
		self.sleepTimer = None
