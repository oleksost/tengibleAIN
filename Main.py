#!/usr/bin/python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import multiprocessing
import threading
#from Webserver import MainHandler
from Webserver import WebSocketHandler

from Participant import Participant
from Bulletin import Bulletin
from Operator import Operator
from Service import Service
from Manufacturer import Manufacturer
import Pump
import time
import json
import datetime
import RPi.GPIO as GPIO
from PIL import Image
import pygame
from multiprocessing import Process, Queue
import signal
from random import randint
import RFID
import signal


# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

OUT_manufacturer=11
OUT_service=15
OUT_operator=12
BREAK_ASSET=40
SERVICE_BULETTE_FABRIK=31
SERVICE_BULETTE_FABRIK_MEASURE=33
SERVICE_BULETTE_CUSTOMER=16
SERVICE_BULETTE_CUSTOMER_MEASURRE=18

greating="Great choice! You just bought the Asset "
pygame.display.init()                 


def get_alife():
     GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
     GPIO.output(Service.GPIO_out, GPIO.HIGH)
     GPIO.output(Operator.GPIO_out, GPIO.HIGH)
     #Participant.show_img("img/1.PNG")
     time.sleep(2)
     GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
     GPIO.output(Service.GPIO_out, GPIO.LOW)
     GPIO.output(Operator.GPIO_out, GPIO.LOW)

 #Calls GPIO cleanup
 #rdr.cleanup()  
             
def ckeck_if_info_bulletin_in_place(GPIO_place):
   
    a = datetime.datetime.now()
    b=datetime.datetime.now()
    dd=b-a
    c=0
    while dd.microseconds<500000 and c<1:
        
         b=datetime.datetime.now()
         dd=b-a
         if GPIO.input(GPIO_place)==1:
              c=c+1
    if not c<1:
         bulletin_in=True
        
    else:
         bulletin_in=False
    return bulletin_in

def running_page():
      templateData = {
      'participant' : "Running",
      'Message': ""
       }
      return render_template('running.html', **templateData)
   
def speak_start():
      templateData = {
      'participant' : "Welcome",
      'Message': ""
       }
      return render_template('index.html', **templateData)
      

def main():
  #running_page()
  GPIO.setup(BREAK_ASSET, GPIO.IN)

  global Manufacturer
  global Service
  global Operator
  Manufacturer=Manufacturer(OUT_manufacturer, SERVICE_BULETTE_FABRIK, SERVICE_BULETTE_FABRIK_MEASURE, bulletin=Bulletin())
  Service=Service(OUT_service)
  Operator=Operator(OUT_operator,SERVICE_BULETTE_CUSTOMER,SERVICE_BULETTE_CUSTOMER_MEASURRE)

  
  #speak_start()
  get_alife()
  #time.sleep(3)
  #protection for multiprocessing, only for Windows
  WebSocketHandler.send_updates("Hello, I am working")
  Operator.buy_asset(Manufacturer)
      
  bulletin_activation=0

  GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)

  #endless loop
  while True:
  
    #check if Info Bulletin is plugged in the manufacturer, false by default and if not activated  
    bulletin_in=ckeck_if_info_bulletin_in_place(Manufacturer.Service_Bulletin_GPIO_Measure)
    
    #checking if the Asset is on the RFID reader
    Operator.check_asset()
    
    if datetime.datetime.now()>Manufacturer.Next_asset_update and not bulletin_in and not Manufacturer.Bulletin.Activated and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulletin.Activated=True
         bulletin_in=True
         Manufacturer.activate_bulletin()
         
    if Manufacturer.Bulletin.Activated and not bulletin_in and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulletin.Activated=False
         Manufacturer.Bulletin_at_campus=False
         GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)  

    if not Manufacturer.Bulletin.Activated and bulletin_in and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.deactivate_bulletin()
         bulletin_in=False
         Manufacturer.Bulletin_at_campus=True
         
    #checking if the received the update from the Bulletin 
    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==1 and not Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Manufacturer.inform_operator_about_Update(Operator)


    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Operator.Informed_about_recent_update=False
         
    #manually break the asset
    if GPIO.input(BREAK_ASSET)==1:
         Operator.Asset_is_working=False
       
    if not Operator.Has_asset:
             #print "No Asset"
             #Protection for multiprocessing, only for Windows
             Operator.buy_asset(Manufacturer)
             #Operator.Asset.set_next_break()   

    if not Operator.Asset.Brocken and not Operator.Asset_is_working:
         WebSocketHandler.send_updates("Asset is broken")
         Operator.Asset.Brocken=True
         Operator.Asset_not_on_RFID=0
         WebSocketHandler.send_updates("Please, repare the Asset!")
         blinker_Queue=Service.blink_service(Service.GPIO_out,0.5)

    #check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
    if Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==0:
               Service.repare_Asset(Operator,blinker_Queue)   
               
     #random asset break
    if datetime.datetime.now()>Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Brocken:
        Operator.Asset_is_working=False

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("index.html")
		threading.Thread(target=main).start()

	def post(self):
		self.render("index.html")  
     
application = tornado.web.Application([
	(r"/", MainHandler),
	#(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(favicon\.ico)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	#(r"/(apple-touch-icon-precomposed\.png)", tornado.web.StaticFileHandler, {'path': '~/yourdir/static'}),
	(r"/websocket", WebSocketHandler),
])      
        
if __name__ == "__main__":
    #comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #app.run(host='0.0.0.0', debug=True)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(5000)
	tornado.ioloop.IOLoop.instance().start()
