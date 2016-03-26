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
global ASSET_INSTALLED

#EVENTS
#1 - installation of  a new aset
#2 - new asset installed, show new asset information
#3 - Asset is brocken
#4 - new update service Bulletin
#5 - Asset repaired
#6 - asset can be pimped 
#7 - Asset is pimped
#8 - Hint event

   
ALARM_manufacturer=15
ALARM_operator=12
ALARM_service=38
PIMP_GPIO=36
OUT_manufacturer=11
OUT_service=15
ALARM_operator=12
BREAK_ASSET=40
SERVICE_BULETTE_MANUFACTURER=31
SERVICE_BULETTE_MANUFACTURER_MEASURE=33
SERVICE_BULETTE_OPERATOR=16
SERVICE_BULETTE_OPERATOR_MEASURRE=18

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
   ALARM_manufacturer=16
   ALARM_operator=12
   ALARM_service=38
   
   BREAK_ASSET=40
   SERVICE_BULETTE_MANUFACTURER=31
   SERVICE_BULETTE_MANUFACTURER_MEASURE=35
   SERVICE_BULETTE_OPERATOR=32
   SERVICE_BULETTE_OPERATOR_MEASURRE=33
   #GPIO.cleanup()
   Manufacturer=Manufacturer(OUT_manufacturer, service_bulletin_out=SERVICE_BULETTE_MANUFACTURER, service_bullete_measure=SERVICE_BULETTE_MANUFACTURER_MEASURE, alarm_out=ALARM_manufacturer, bulletin=Bulletin())
   Service=Service(OUT_service, alarm_out=ALARM_service)
   Operator=Operator(service_bulletin_out=SERVICE_BULETTE_OPERATOR, service_bullete_measure=SERVICE_BULETTE_OPERATOR_MEASURRE, alarm_out=ALARM_operator, pimp_gpio=PIMP_GPIO)
   GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
   GPIO.output(Manufacturer.Service_Bulletin_GPIO_out, GPIO.LOW)
   GPIO.output(Manufacturer.ALARM_out, GPIO.LOW)
   GPIO.output(Operator.ALARM_out, GPIO.LOW)
   GPIO.output(Service.ALARM_out, GPIO.LOW)
   
   global ASSET_INSTALLED
   
 
 
   GPIO.setup(BREAK_ASSET, GPIO.IN)
   get_alife(Manufacturer.GPIO_out,Service.GPIO_out,Operator.Service_Bulletin_GPIO_out)
   
   Participant.update_event(0)
   
   GPIO.output(Operator.ALARM_out, GPIO.HIGH)
   Operator.buy_asset(Manufacturer, queue)
   
   #ASSET_INSTALLED=True
   #GPIO.output(self.ALARM_out, GPIO.LOW)
   
   #Variables for the service car handling
   servicecar_was_at_the_operators_facility=False
   reminded_4=False
   reminded_3=False
   #######################################
   #Variable for the handling of the asset boosting
   reminded_5=False
   ###keeping track on hints, starting always with an empty hint display####
   current_hint=1
   
   broken_count_securit=0
   broken_count_securit_last=0
   
   
   first_pimp=True
   INFORMED_BULLETIN=False
   
   informed_to_remove_he_service_car=False
   service_car_stays_at_operators=0
   next_hint_to_remove_service_car=0
   
   pimping=0
   
   while queue.empty():
   
    #checking if the Asset is on the RFID reader
    Operator.check_asset()
    
    if Operator.Has_asset and ASSET_INSTALLED and not Operator.Asset.Brocken and Operator.Has_asset:
    ##BULLETIN HANDLING###  
      if not Manufacturer.Next_asset_update==0:
        if datetime.datetime.now()>Manufacturer.Next_asset_update and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==0 and not Manufacturer.Bulletin.Activated:
         Manufacturer.Bulletin.Activated=True
         Manufacturer.Bulletin_at_campus=True
         Participant.update_event(9)
         GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)   
         Manufacturer.activate_bulletin(queue)
      else:
         Manufacturer.set_next_asset_update_time(1)
         
      if Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==0 and not Manufacturer.Bulletin_at_campus:
         Manufacturer.activate_bulletin(queue)
         Manufacturer.Bulletin_at_campus=True

         
      if Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==1 and Manufacturer.Bulletin_at_campus:
         Manufacturer.deactivate_bulletin()
         GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
         Manufacturer.Bulletin_at_campus=False
         
      if not Manufacturer.Next_asset_update ==0:
       if datetime.datetime.now()>Manufacturer.Next_asset_update and GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and Manufacturer.Bulletin.Activated and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure)==1 and not Manufacturer.Bulletin_at_campus:
         print "Informing"
         if not Operator.Informed_about_recent_update:
             Participant.update_event(4)
             Operator.Informed_about_recent_update=True
             GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
             time.sleep(2)
             GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
         Manufacturer.inform_operator_about_Update(Operator)
             
    ##END BULLETIN HANDLING###  
    #ASSET BREAK
    if Operator.Has_asset and ASSET_INSTALLED and Operator.Asset.Pimped and not Operator.Asset.Brocken:
      if Operator.Asset.Next_Break==0:
       Operator.Asset.set_next_break()
      #MANUAL BREAK
      #print broken_count_securit
      if GPIO.input(BREAK_ASSET)==0:
         broken_count_securit=0
         
      if GPIO.input(BREAK_ASSET)==1:
         #broken_count_securit_last=1
         broken_count_securit=broken_count_securit+1
      if GPIO.input(BREAK_ASSET)==0:
         broken_count_securit=0
      if broken_count_securit>5 and not Operator.Asset.Brocken and Operator.Has_asset and Manufacturer.Bulletin.Activated and not Manufacturer.Bulletin_at_campus:
         Operator.Asset_is_working=False
         broken_count_securit=0
       
      #RANDOM ASSET BREAK
      if not Operator.Asset.Next_Break==0:
       if datetime.datetime.now()>Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Brocken and Operator.Has_asset:
         print "not working"
         Operator.Asset_is_working=False   
         
    if not Operator.Has_asset and ASSET_INSTALLED:
             print "No Asset"
             if not Operator.Informed_about_recent_update:
               Manufacturer.Bulletin.Activated=False
             Manufacturer.deactivate_bulletin()
             Manufacturer.Next_asset_update=0
             GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
             GPIO.output(Service.GPIO_out, GPIO.LOW)
             ASSET_INSTALLED=False
             INFORMED_BULLETIN=False
             #Operator.Informed_about_recent_update=False
             Operator.Asset.Next_Pimp=0
             Operator.Asset.Next_Break=0
             first_pimp=True
             GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
             Participant.update_event(1)
             Operator.buy_asset(Manufacturer, queue)
             #Operator.Asset.set_next_break()   
    
    
    if not Operator.Asset.Brocken and not Operator.Asset_is_working and ASSET_INSTALLED and Operator.Has_asset:
         Participant.update_event(3)
         Operator.Asset.Brocken=True
         Operator.Asset_not_on_RFID=0
         global blinker_Queue
         #blink ALL
         blinker_Queue_Service=Participant.blink_service(Service.ALARM_out,0.5, queue)       
         blinker_Queue_Operator=Participant.blink_service(Operator.ALARM_out,0.5, queue)         
         blinker_Queue_Manufacturer=Participant.blink_service(Manufacturer.ALARM_out,0.5, queue)         
    
    
        
    ##HANDLING THE SERVICE CAR AND REPAIRING THE ASSET## 
    if GPIO.input(Operator.Asset.GPIO_to_repair)==0 and service_car_stays_at_operators<=3:
         service_car_stays_at_operators+=1
    if GPIO.input(Operator.Asset.GPIO_to_repair)==1 and service_car_stays_at_operators>=-6:
         service_car_stays_at_operators-=1

    #check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
    if Operator.Asset.Brocken and service_car_stays_at_operators>2:
               #stop blinking ALL
               Service.repare_Asset(Operator,blinker_Queue_Service,blinker_Queue_Operator,blinker_Queue_Manufacturer)
               next_hint_to_remove_service_car=datetime.datetime.now()+datetime.timedelta(seconds=20)
               informed_to_remove_he_service_car=False
               
    if service_car_stays_at_operators<0:
               next_hint_to_remove_service_car=0
               if informed_to_remove_he_service_car:
                     Participant.update_event(12)
                     GPIO.output(Service.GPIO_out, GPIO.LOW)
                     informed_to_remove_he_service_car=False
               
    if not next_hint_to_remove_service_car==0:               
      if not Operator.Asset.Brocken and service_car_stays_at_operators>5 and datetime.datetime.now()>next_hint_to_remove_service_car:
               #hint: place the service car back to the service station
               Participant.update_event(11)
               GPIO.output(Service.GPIO_out, GPIO.HIGH)
               informed_to_remove_he_service_car=True
               next_hint_to_remove_service_car=datetime.datetime.now()+datetime.timedelta(seconds=20)
    ### END HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##
    
             
    if ASSET_INSTALLED and not Operator.Asset.Brocken and Operator.Has_asset:
    ####HANDLING ASSET PIMPING#######
     if GPIO.input(Operator.Pimp_GPIO)==1 and pimping<=8:
         pimping+=1
     
     if GPIO.input(Operator.Pimp_GPIO)==0 and pimping>=-7:
         pimping-=1   
     #remind to pimp the asset                     
     if not Manufacturer.Bulletin_at_campus and GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0:
      if first_pimp and Operator.Asset.Next_Pimp==0 and not Operator.Asset.Pimped:
        #print "handle"
        #print Operator.Asset.Pimped
        Operator.Asset.set_next_pimp_reminder(seconds_=8)
        
        if pimping<5:
               Operator.Asset.Pimped=False
                
      if not Operator.Asset.Next_Pimp==0:      
       if datetime.datetime.now()>Operator.Asset.Next_Pimp and not Operator.Asset.Pimped and not Operator.Asset.Brocken and Operator.Has_asset:
               Participant.update_event(10)
               GPIO.output(Service.GPIO_out, GPIO.HIGH)
               Operator.Asset.Next_Pimp=0
               if first_pimp:
                first_pimp=False
               
     ####Pimping the asset
              
     if pimping>7 and not Operator.Asset.Pimped and not INFORMED_BULLETIN:
               Operator.pimp_the_pump()
               INFORMED_BULLETIN=True
               GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
               GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
               GPIO.output(Service.GPIO_out, GPIO.HIGH)
               time.sleep(2)
               GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
               GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
               GPIO.output(Service.GPIO_out, GPIO.LOW)
               
               
     if pimping==0 and Operator.Asset.Pimped and not Operator.Asset.Brocken and Operator.Has_asset:
               Operator.unpimp_the_pump()
               GPIO.output(Service.GPIO_out, GPIO.HIGH)
               time.sleep(2)
               GPIO.output(Service.GPIO_out, GPIO.LOW)
               INFORMED_BULLETIN=False
               Operator.Asset.Next_Break=0
               Operator.Asset.set_next_pimp_reminder()
               #reminded_5=False

   print "stoped"
   
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
            
            global Main_Queue
            global main_thread
            #print("button click")
            #check if everythings in place
            (ready, msg)=check_ready_to_start()
            if threading.active_count()<10:
              print "starting..."
              Main_Queue=Queue()
              main_thread=threading.Thread(target=main, args=(1,Main_Queue))
              main_thread.daemon = True
              main_thread.start()
              #main_thread.join()
              
            
class StopHandler(tornado.web.RequestHandler):
         def get(self):
            #GPIO.cleanup()
            #GPIO.setmode(GPIO.BOARD)
            print "Attempting to stop"
            try:
              Main_Queue.put("Stop")
              print str(threading.enumerate())
              #while threading.active_count()>1:
               # print threading.active_count()
              
              
            except NameError:
              print "nothing to stop"
               
         def post(self):
            #GPIO.cleanup()
            #GPIO.setmode(GPIO.BOARD)
            print "Attempting to stop"
            try:
              Main_Queue.put("Stop")
              print str(threading.enumerate())
            except NameError:
              print "nothing to stop"
              
class InstalledHandler(tornado.web.RequestHandler):
         def get(self):
           global ASSET_INSTALLED
           print "setting intalled"
           if ASSET_INSTALLED==False:
            ASSET_INSTALLED=True
     
         def post(self):
           print "setting intalled"
           global ASSET_INSTALLED
           if ASSET_INSTALLED==False:
            ASSET_INSTALLED=True
           
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    
application = tornado.web.Application([ 
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/start/", StartHandler),
    (r"/stop/", StopHandler),
    (r"/asset_installed/", InstalledHandler),
    #(r"/get_content_xml/", XMLLoader),
],debug=True, **settings)

        
if __name__ == "__main__":
  try:
    global ASSET_INSTALLED
    ASSET_INSTALLED=False
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
