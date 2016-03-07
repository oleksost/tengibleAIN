import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import os
import time
import multiprocessing
import json
import RPi.GPIO as GPIO
import threading
GPIO.setmode(GPIO.BOARD)

class Button():
	def __init__(self, gpio):
	  self.GPIO=gpio
	  GPIO.setup(gpio, GPIO.IN)
	  GPIO.setmode(GPIO.BOARD)
	  
	def pressed(self):
	   pressed =False
	   if GPIO.input(self.GPIO)==1:
	     pressed = True
	   return pressed
	     
	   
			
def ButtonMonitor():
	index = 50
	button = Button(32)
	#repo = Repository.Repository()
	#index = int(repo.get_current_count())
	print str(index)
	while 1:
		if button.pressed():
			index -= 1
			if index < 0:
				index = 50
			print str(index)
			#repo.set_count(index)
		time.sleep(0.05)
	
if __name__ == "__main__":
	ButtonMonitor()