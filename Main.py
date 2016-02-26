#!/usr/bin/python
import Participant
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

rdr=RFID.RFID()
util = rdr.util()

ASSET_1 = 36
ASSET_2 = 38
ASSET_3 = 40
BREAK_ASSET=40
OUT_manufacturer=11
OUT_service=15
OUT_operator=12
SERVICE_BULETTE=31
SERVICE_BULETTE_FABRIK=33
SERVICE_BULETTE_CUSTOMER=16
SERVICE_BULETTE_CUSTOMER_MEASURRE=18

OUT_Pump_Plug=16
OUT_Pump_Plug_Service=7

greating="Great choice! You just bought the Asset "
pygame.display.init()                 

GPIO.setup(OUT_Pump_Plug, GPIO.OUT)
GPIO.setup(OUT_Pump_Plug_Service, GPIO.OUT)
GPIO.setup(SERVICE_BULETTE, GPIO.OUT)
GPIO.setup(SERVICE_BULETTE_CUSTOMER, GPIO.OUT)

GPIO.setup(ASSET_1, GPIO.IN)
GPIO.setup(ASSET_2, GPIO.IN)
GPIO.setup(ASSET_3, GPIO.IN)
GPIO.setup(BREAK_ASSET, GPIO.IN)
GPIO.setup(SERVICE_BULETTE_FABRIK, GPIO.IN)
GPIO.setup(SERVICE_BULETTE_CUSTOMER_MEASURRE, GPIO.IN)

#Pump_1=Pump.Pump(215, "Pump1", ASSET_1, False, None)
#Pump_2=Pump.Pump(138, "Pump2", ASSET_2, False, None)


manufacturer=Participant.Participant(OUT_manufacturer)
service=Participant.Participant(OUT_service)
operator=Participant.Participant(OUT_operator)

def get_alife():
     GPIO.output(manufacturer.OUT, GPIO.HIGH)
     GPIO.output(service.OUT, GPIO.HIGH)
     GPIO.output(operator.OUT, GPIO.HIGH)
     show_img("img/1.PNG")
     time.sleep(2)
     GPIO.output(OUT_manufacturer, GPIO.LOW)
     GPIO.output(OUT_service, GPIO.LOW)
     GPIO.output(OUT_operator, GPIO.LOW)

def show_img(img):
    imgSurf = pygame.image.load(img)
    imgSurf=pygame.transform.scale(imgSurf,(1280,1024))
    screen = pygame.display.set_mode(imgSurf.get_size())
    screen.blit (imgSurf,(0,0))
    pygame.display.flip()

def buy_pump():
     print greating + str(Asset.Name)
     show_img("img/2.PNG")
     time.sleep(3)
     show_img("img/3.PNG")
     time.sleep(3)
     
def buying_pump():
    if __name__== '__main__':
       q=Queue()
       p=Process(target=activate_actor, args=(OUT_operator,q, 0.5))
       p.start()
    print "Operator: I need to buy a new pump!"
    global isBought
    isBought = False
    global asset_id
    asset_id =0
    while not isBought:
      readRFID()
      if Asset.RFID_Identifier>0 and not isBought:
        buy_pump()
        q.put("Stop")
        p.terminate()
        isBought=True
        show_img("img/1.PNG")

def activate_actor(actor,q, frequenz):
    
    while q.empty():
      # LED an
      GPIO.output(actor, GPIO.HIGH)
      # Warte 100 ms
      time.sleep(frequenz)
      # LED aus
      GPIO.output(actor, GPIO.LOW)
      # Warte 100 ms
      time.sleep(frequenz)
      
def breake():
     GPIO.output(OUT_Pump_Plug, GPIO.LOW)

def readRFID():
 global Asset
 global rdr
 global util
 rdr=RFID.RFID()
 util = rdr.util()
 
 while True:
  (error, tag_type) = rdr.request()
  if not error:
    #print "Tag detected"
    (error, uid) = rdr.anticoll()
    if not error:
         #print "UID: " + str(uid[1])
         if uid[1]==215:
              Asset=Pump.Pump(uid[1], "Pump1", ASSET_1, False, None)
              break
         if uid[1]==138:
              Asset=Pump.Pump(uid[1], "Pump2", ASSET_2, False, None)
              break

          
 #Calls GPIO cleanup
 #rdr.cleanup()  
          
get_alife()
time.sleep(3)
GPIO.output(OUT_Pump_Plug, GPIO.HIGH)
GPIO.output(OUT_Pump_Plug_Service, GPIO.HIGH)
buying_pump()
(error, tag_type) = rdr.request()

  
def blink_service(gpio, queue, frequenz):
    pr=Process(target=activate_actor, args=(gpio,queue,frequenz))
    pr.start()

# count how many loop rounds asset is not on the RFID reader in variable asset_on_RFID  
asset_on_RFID = 0
bulletin_activation=0
user_bulleting_deactivation=0

#work()
finished_working=False
bulette_fabrik_activated=False
bulette_fabrik_removed=False
user_informed_about_bulette=False
bulette_in=False

GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)


#endless loop
while True:

    if GPIO.input(SERVICE_BULETTE_CUSTOMER_MEASURRE)==1 and not user_informed_about_bulette and not Asset.Brocken:
         print "New data from Service Bulette"
         user_informed_about_bulette=True
         time.sleep(2)
         GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.LOW)
         

    if GPIO.input(SERVICE_BULETTE_CUSTOMER_MEASURRE)==0 and user_informed_about_bulette and not Asset.Brocken:
         #GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)
         user_informed_about_bulette=False
    
    
    #bulette_in=False
    a = datetime.datetime.now()
    b=datetime.datetime.now()
    dd=b-a
    c=0
    while dd.microseconds<500000 and c<1:
        
         b=datetime.datetime.now()
         dd=b-a
         if GPIO.input(SERVICE_BULETTE_FABRIK)==1:
              c=c+1
    if not c<1:
         bulette_in=True
        
    else:
         bulette_in=False
     
    if not Asset.Brocken:
         (error, tag_type) = rdr.request()

    #if bulletin_activation>50 and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not bulette_fabrik_activated and not bulette_fabrik_removed and not asset_broken:
    if bulletin_activation>10 and not bulette_in and not bulette_fabrik_activated and not bulette_fabrik_removed and not Asset.Brocken:
         bulette_fabrik_activated=True
         bulette_in=True
         global queue_bulette
         queue_bulette=Queue()
         blink_service(SERVICE_BULETTE, queue_bulette, 0.3)
         #GPIO.output(SERVICE_BULETTE, GPIO.HIGH)
         #bulletin_activation=0
         
    #if bulletin_activation<=50 and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not asset_broken:
    if bulletin_activation<=10 and not bulette_in and not Asset.Brocken:
         #print str(bulletin_activation)
         bulletin_activation=bulletin_activation+1
         

    #if bulette_fabrik_activated==True and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not bulette_fabrik_removed and not asset_broken:
    if bulette_fabrik_activated==True and not bulette_in and not bulette_fabrik_removed and not Asset.Brocken:
         #print "HAllo"
         bulette_fabrik_activated=False
         bulette_fabrik_removed=True
         GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)

    #if bulette_fabrik_activated==False and GPIO.input(SERVICE_BULETTE_FABRIK)==1 and bulette_fabrik_removed and not asset_broken:
    if bulette_fabrik_activated==False and bulette_in and bulette_fabrik_removed and not Asset.Brocken:
         queue_bulette.put("Stop")
         bulette_in=False
         #GPIO.output(SERVICE_BULETTE, GPIO.LOW)
         #bulette_fabrik_activated=False
         bulette_fabrik_removed=False
         bulletin_activation=0

         
    #increase the round number only if the asset is not on the RFID reader several loop round in sequence (due to the RFID signal instability)
    if error and not Asset.Brocken:
         asset_on_RFID=asset_on_RFID+1
    else:
         asset_on_RFID=0

    if GPIO.input(BREAK_ASSET)==1:
         finished_working=True
     
    #if not queue_Asset_Working.empty():
         #finished_working=True

    if asset_on_RFID>2: 
         isBought=False
        
    if not isBought:
        buying_pump()
        asset_on_RFID=0
        finished_working=False
        #work()

    if not Asset.Brocken and finished_working:
         print "Asset is broken"
         Asset.Brocken=True
         print "Repare the Asset!"
         asset_on_RFID=0
         #global qu
         #qu=Queue()
         service.blink_service(0.5)
         finished_working=False
         
    if Asset.Brocken:
          if GPIO.input(Asset.GPIO_to_repair)==1:
               Asset.Brocken=False
               asset_on_RFID=0
               service.stop_blink_service()
               print "Congratulations, you repaired the Asset!"
               finished_working=False
               #work()
    
