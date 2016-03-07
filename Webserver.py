import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import multiprocessing
import threading


		
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