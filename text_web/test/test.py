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
	     
	   

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("index.html")

	def post(self):
		self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	waiters = set()
 
	def open(self):
		self.set_nodelay(True)
		print('Socket Connected: ' + str(self.request.remote_ip))
		#repo = Repository.Repository()
		#self.write_message(str(repo.get_current_count()))
		WebSocketHandler.waiters.add(self)
 
	def on_close(self):
		WebSocketHandler.waiters.remove(self)
 
	@classmethod
	def send_updates(cls, index):
		for waiter in cls.waiters:
			try:
				waiter.write_message(index)
			except:
				print("Error sending message")
				
def ButtonMonitor():
	index = 50
	button = Button(32)
	#repo = Repository.Repository()
	#index = int(repo.get_current_count())
	WebSocketHandler.send_updates(str(index))
	while 1:
		if button.pressed():
			index -= 1
			if index < 0:
				index = 50
			WebSocketHandler.send_updates(str(index))
			#repo.set_count(index)
		time.sleep(0.5)
		
application = tornado.web.Application([
	(r"/", MainHandler),
	#(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(favicon\.ico)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(apple-touch-icon-precomposed\.png)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	(r"/websocket", WebSocketHandler),
])		
		
if __name__ == "__main__":
	threading.Thread(target=ButtonMonitor).start()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(5000)
	tornado.ioloop.IOLoop.instance().start()