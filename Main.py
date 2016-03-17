#!/usr/bin/python
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import multiprocessing
import threading
from Webserver import WebSocketHandler
from Webserver import MainHandler
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
#import pygame
from multiprocessing import Process, Queue
import signal
from random import randint
import RFID

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

#EVENTS
#1 - installation of  a new aset
#2 - new asset installed, show new asset information
#3 - Asset is brocken
#4 - new update service Bulletin
#5 - Asset repaired
#6 - asset can be pimped 
#7 - Asset is pimped
#8 - Hint event

#HINTS
#1 - clean the hint display
#2 - bulletin should be moved to the manufacturer for the verification at the beginning of the demo
#3 - service car should be moved back to the service station
#4 - reminder to bring back the car
#5 - asset can be pimped
#6 - bulleting is activated and should be brought to the operator

PIMP_GPIO=36
OUT_manufacturer=11
OUT_service=15
OUT_operator=12
BREAK_ASSET=40
SERVICE_BULETTE_FABRIK=31
SERVICE_BULETTE_FABRIK_MEASURE=33
SERVICE_BULETTE_CUSTOMER=16
SERVICE_BULETTE_CUSTOMER_MEASURRE=18

#pygame.display.init()     

def get_alife(Manufacturer_GPIO_out,Service_GPIO_out,Operator_GPIO_out):
     print str(Manufacturer_GPIO_out)
     print str(Service_GPIO_out)
     print str(Operator_GPIO_out)
     GPIO.output(Manufacturer_GPIO_out, GPIO.HIGH)
     GPIO.output(Service_GPIO_out, GPIO.HIGH)
     GPIO.output(Operator_GPIO_out, GPIO.HIGH)
     #Participant.show_img("img/1.PNG")
     time.sleep(2)
     GPIO.output(Manufacturer_GPIO_out, GPIO.LOW)
     GPIO.output(Service_GPIO_out, GPIO.LOW)
     GPIO.output(Operator_GPIO_out, GPIO.LOW)

 #Calls GPIO cleanup
 #rdr.cleanup()

"""
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
"""

def main(a,queue):
  try:
  
   import os
   import tornado.httpserver
   import tornado.ioloop
   import tornado.web
   import tornado.websocket
   import tornado.gen
   from tornado.options import define, options
   import multiprocessing
   import threading
   from Webserver import WebSocketHandler
   from Webserver import MainHandler
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
   GPIO.setmode(GPIO.BOARD)
  
   PIMP_GPIO=36
   OUT_manufacturer=11
   OUT_service=15
   OUT_operator=12
   BREAK_ASSET=40
   SERVICE_BULETTE_FABRIK=31
   SERVICE_BULETTE_FABRIK_MEASURE=35
   SERVICE_BULETTE_CUSTOMER=32
   SERVICE_BULETTE_CUSTOMER_MEASURRE=33
   #GPIO.cleanup()
   Manufacturer=Manufacturer(OUT_manufacturer, service_bulletin_out=SERVICE_BULETTE_FABRIK, service_bullete_measure=SERVICE_BULETTE_FABRIK_MEASURE, bulletin=Bulletin())
   Service=Service(OUT_service)
   Operator=Operator(gpio_out=OUT_operator, service_bulletin_out=SERVICE_BULETTE_CUSTOMER, service_bullete_measure=SERVICE_BULETTE_CUSTOMER_MEASURRE, pimp_gpio=PIMP_GPIO)
   GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
   GPIO.output(Manufacturer.Service_Bulletin_GPIO_out, GPIO.LOW)
 
 
   GPIO.setup(BREAK_ASSET, GPIO.IN)
   get_alife(Manufacturer.GPIO_out,Service.GPIO_out,Operator.GPIO_out)
   Operator.buy_asset(Manufacturer, queue)
   
   #Variables for the service car handling
   servicecar_was_at_the_operators_facility=False
   reminded_4=False
   reminded_3=False
   #######################################
   #Variable for the handling of the asset boosting
   reminded_5=False
   ###keeping track on hints, starting always with an empty hint display####
   current_hint=1
   
   while queue.empty():
    #checking if the Asset is on the RFID reader
    Operator.check_asset()
    
    """
        #check if Info Bulletin is plugged in the manufacturer, false by default and if not activated  
    bulletin_in=ckeck_if_info_bulletin_in_place(Manufacturer.Service_Bulletin_GPIO_Measure)
 
    if datetime.datetime.now()>Manufacturer.Next_asset_update and not bulletin_in and not Manufacturer.Bulletin.Activated and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulletin.Activated=True
         print ("Bulleting activated, bring it to the operator")
         bulletin_in=True
         Manufacturer.activate_bulletin(queue)
         GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
         
    if Manufacturer.Bulletin.Activated and not bulletin_in and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         #Manufacturer.Bulletin.Activated=False
         bulletin_in=False
         Manufacturer.Bulletin_at_campus=False
         #GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
         
    if Manufacturer.Bulletin.Activated and bulletin_in and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
       print ("Bring activated Bulletinn to the operator")
       Manufacturer.Bulletin_at_campus=True
       
    if not Manufacturer.Bulletin_at_campus:
        Manufacturer.check_bulletin();
        
    #if not Manufacturer.Bulletin.Activated and bulletin_in and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
     #    Manufacturer.deactivate_bulletin()
      #   bulletin_in=False
       #  Manufacturer.Bulletin_at_campus=True
         
    #checking if the received the update from the Bulletin 
    if datetime.datetime.now()>Manufacturer.Next_asset_update and not bulletin_in and Manufacturer.Bulletin.Activated and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         #Manufacturer.Bulletin.Activated=True
         #bulletin_in=True
         #Manufacturer.activate_bulletin(queue)
         GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
    
    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==1 and Manufacturer.Bulletin.Activated and not Manufacturer.Bulletin_at_campus and not Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Manufacturer.inform_operator_about_Update(Operator)
         #Manufacturer.Bulletin.Activated=False
         #Manufacturer.Bulletin_at_campus=True
         
         
    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Operator.Informed_about_recent_update=False
    """
    ##BULLETIN HANDLING###  
    if datetime.datetime.now()>Manufacturer.Next_asset_update and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==0 and not Manufacturer.Bulletin.Activated and not Operator.Asset.Brocken and Operator.Has_asset:
         Manufacturer.Bulletin.Activated=True
         Manufacturer.Bulletin_at_campus=True
         #activated, bring to the operator
         Participant.update_event(8, hint_id=6)
         current_hint=6
         Manufacturer.activate_bulletin(queue)
         reminded_5=False
         
    if Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==0 and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken and Operator.Has_asset:
         Manufacturer.activate_bulletin(queue)
         Manufacturer.Bulletin_at_campus=True
         Participant.update_event(8, hint_id=1)
         current_hint=1
         
    if Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==1 and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken and Operator.Has_asset:
         Manufacturer.deactivate_bulletin()
         Manufacturer.Bulletin_at_campus=False
         Participant.update_event(8, hint_id=1)
         current_hint=1
         
    if datetime.datetime.now()>Manufacturer.Next_asset_update and GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==1 and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         print "Informing"
         Manufacturer.inform_operator_about_Update(Operator)
    ##END BULLETIN HANDLING###  
    
    #manually break the asset
    if GPIO.input(BREAK_ASSET)==1 and not Operator.Asset.Brocken and Operator.Has_asset:
         Operator.Asset_is_working=False
       
    if not Operator.Has_asset:
             print "No Asset"
             #if Manufacturer.Bulletin.Activated:
              # Manufacturer.deactivate_bulletin()
             #print ("Bulleting deactivating")
             Operator.buy_asset(Manufacturer, queue)
             #Operator.Asset.set_next_break()   
             
    if not Operator.Asset.Brocken and not Operator.Asset_is_working:
         Participant.update_event(3)
         Operator.Asset.Brocken=True
         Operator.Asset_not_on_RFID=0
         #WebSocketHandler.send_updates("Please, repare the Asset!")
         global blinker_Queue
         blinker_Queue=Service.blink_service(Service.GPIO_out,0.5, queue)
        
    #random asset break
    if datetime.datetime.now()>Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Brocken and Operator.Has_asset:
               Operator.Asset_is_working=False
         
    ##HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##
    #check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
    if Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==0 and not servicecar_was_at_the_operators_facility:
               Service.repare_Asset(Operator,blinker_Queue)
               servicecar_was_at_the_operators_facility=True
               #clean the hint notification
               Participant.update_event(8, hint_id=1)
               current_hint=1
               #reminded_4=False
               reminded_3=False
               reminded_5=False
               
    if not Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==1 and servicecar_was_at_the_operators_facility:
               #clean the hint notification
               Participant.update_event(8, hint_id=1)
               current_hint=1
               #setting the next break time for the asset only after the service car is away
               Operator.Asset.set_next_break()
               servicecar_was_at_the_operators_facility=False
               reminded_5=False   
    if not Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==0 and servicecar_was_at_the_operators_facility and not reminded_3:
               #hint: place the service car back to the service station
               Participant.update_event(8, hint_id=3)
               current_hint=3
               reminded_3=True
               reminded_5=False       
     #if the service car has not been removed from operators facilities since last break
    #if Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==0 and servicecar_was_at_the_operators_facility and not reminded_4:
               #reminder hint to place the service car back to the service station
     #          Participant.update_event(8, hint_id=4)
      #         reminded_4=True
       #        reminded_5=False
    
               

               
    if Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==1 and servicecar_was_at_the_operators_facility:
               servicecar_was_at_the_operators_facility=False 
               Participant.update_event(8, hint_id=1)   
               current_hint=1
    ### END HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##
    
    
    ####HANDLING ASSET PIMPING#######
    #remind to pimp the asset
    if datetime.datetime.now()>Operator.Asset.Next_Pimp and current_hint==1 and not Operator.Asset.Pimped and not reminded_5 and not Operator.Asset.Brocken and Operator.Has_asset:
              #hint priority handling
              if current_hint==1 or current_hint==3:
               Participant.update_event(8, hint_id=5)
               current_hint=5
               reminded_5=True
               
    ####Pimping the asset
    if GPIO.input(Operator.Pimp_GPIO)==1 and not Operator.Asset.Pimped and not Operator.Asset.Brocken and Operator.Has_asset:
               Operator.pimp_the_pump()
               #clean the hint display
               Participant.update_event(8, hint_id=1)
               current_hint=1
               
    if GPIO.input(Operator.Pimp_GPIO)==0 and Operator.Asset.Pimped and not Operator.Asset.Brocken and Operator.Has_asset:
               Operator.unpimp_the_pump()
               Operator.Asset.set_next_pimp_reminder()
               reminded_5=False

   print "stoped"
   #blinker_Queue.put("stop")
   #Participant.stop_blink_service(Manufacturer.blinker_Queue)  
   #Participant.stop_blink_service(blinker_Queue)
   
  except KeyboardInterrupt:  
    # here you put any code you want to run before the program  
    # exits when you press CTRL+C
    GPIO.cleanup()
    http_server.stop()
  #except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    #print "Other error or exception occurred!"  
  
  finally:  
    GPIO.cleanup() # this ensures a clean exit  
#and main method



def check_ready_to_start():
    ready=True
    msg=""
    return (ready, msg)

class StartHandler(tornado.web.RequestHandler):
     def get(self):
            #GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            global qu
            global main_thread
            #print("button click")
            #check if everythings in place
            (ready, msg)=check_ready_to_start()
            if threading.active_count()<4:
              qu=Queue()
              main_thread=threading.Thread(target=main, args=(1,qu))
              main_thread.daemon = True
              main_thread.start()
              #main_thread.join()
              
            
class StopHandler(tornado.web.RequestHandler):
         def get(self):
            #GPIO.cleanup()
            #GPIO.setmode(GPIO.BOARD)
            print "Attempting to stop"
            try:
              qu.put("Stop")
              print str(threading.enumerate())
              #while threading.active_count()>1:
               # print threading.active_count()
              
              
            except NameError:
              print "nothing to stop"
     

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    
application = tornado.web.Application([ 
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/start/", StartHandler),
    (r"/stop/", StopHandler),
    #(r"/get_content_xml/", XMLLoader),
],debug=True, **settings)

        
if __name__ == "__main__":
  try:
    tornado.httpserver.HTTPServer.allow_reuse_address = True
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.allow_reuse_address = True
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    #print"here is an interrupt 2"
    tornado.ioloop.IOLoop.instance().stop()
    http_server.stop()
    GPIO.cleanup()
  #except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    #print "Other error or exception occurred!"
    #http_server.stop()
    #GPIO.cleanup() 
   
  finally:
    http_server.stop()
    GPIO.cleanup()
