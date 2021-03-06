#!/usr/bin/env python

import pygame
import time
import os
import ArduinoInterface as at

from subprocess import call
from time import sleep

class PS3_Controller:
	
	def __init__(self):
		self.j = None
		self.buttons = {
			"axis" : 0,
			"cruise": 0,
			"ps" : 0
			}
	
	def update_buttons(self):
		events = pygame.event.get()
		
		if events is not None:
			for event in events:
				if event.type == pygame.JOYAXISMOTION:
					if event.axis == 3:
						self.buttons["axis"] = event.value
					if event.axis == 1:
						self.buttons["axis"] = event.value
				if event.type == pygame.JOYBUTTONDOWN:
					if event.button == 8:
						self.buttons["cruise"] = 1
					if event.button == 11:
						self.buttons["cruise"] = 1
				if event.type == pygame.JOYBUTTONUP:
					if event.button == 8:
						self.buttons["cruise"] = 0
					if event.button == 11:
						self.buttons["cruise"] = 1
					
	def check_if_connected(self):
		try:
			result = os.system("ls /dev/input/js*")
			if result == 0:
				self.j = pygame.joystick.Joystick(0)
				self.j.init()
				return True
			else:
				self.j = None
				return False
		except:
			print("exception in check_if_connected")
			return False
	
	def wait_for_connection(self):
		while self.check_if_connected == False:
			print("waiting for connection")
			sleep(.5)
		return True
			
if __name__=="__main__":
	pygame.init()
	os.putenv('SDL_VIDEODRIVER','fbcon')
	pygame.display.init()	
	
	sleep(5.0)
	controller = PS3_Controller()
	currentSpeed = 0
	
	while True:
		if controller.check_if_connected():		
			controller.update_buttons()
			
			newSpeed = int(float(controller.buttons["axis"]) * -100)
			if(controller.buttons["cruise"] == 0):
				if(newSpeed - currentSpeed >= 1 or currentSpeed - newSpeed >= 1):
					print("changing speed: " + str(newSpeed))
					currentSpeed = newSpeed
					at.ChangeSpeed(currentSpeed)
			else:
				print("cruisin")
		else:
			print("no controller connected")
			
			
		sleep(.2)
	
