#!/usr/bin/python
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
ASSET_BROCKEN=40
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

GPIO.setup(OUT_manufacturer, GPIO.OUT)
GPIO.setup(OUT_service, GPIO.OUT)
GPIO.setup(OUT_operator, GPIO.OUT)
GPIO.setup(OUT_Pump_Plug, GPIO.OUT)
GPIO.setup(OUT_Pump_Plug_Service, GPIO.OUT)
GPIO.setup(SERVICE_BULETTE, GPIO.OUT)
GPIO.setup(SERVICE_BULETTE_CUSTOMER, GPIO.OUT)

GPIO.setup(ASSET_1, GPIO.IN)
GPIO.setup(ASSET_2, GPIO.IN)
GPIO.setup(ASSET_3, GPIO.IN)
GPIO.setup(ASSET_BROCKEN, GPIO.IN)
GPIO.setup(SERVICE_BULETTE_FABRIK, GPIO.IN)
GPIO.setup(SERVICE_BULETTE_CUSTOMER_MEASURRE, GPIO.IN)

def get_alife():
     GPIO.output(OUT_manufacturer, GPIO.HIGH)
     GPIO.output(OUT_service, GPIO.HIGH)
     GPIO.output(OUT_operator, GPIO.HIGH)
     show_img("1.PNG")
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

def buy_pump(pump_id):
     print greating + str(pump_id)
     show_img("2.PNG")
     time.sleep(3)
     show_img("3.PNG")
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
      if asset_id>0 and not isBought:
        buy_pump(asset_id)
        q.put("Stop")
        p.terminate()
        isBought=True
        show_img("1.PNG")

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
 global Pump
 global asset_id 
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
              Pump=ASSET_1
              asset_id=1
              break
         if uid[1]==138:
              Pump=ASSET_2
              asset_id=2
              break

          
 #Calls GPIO cleanup
 #rdr.cleanup()  
          
get_alife()
time.sleep(3)
GPIO.output(OUT_Pump_Plug, GPIO.HIGH)
GPIO.output(OUT_Pump_Plug_Service, GPIO.HIGH)
buying_pump()
(error, tag_type) = rdr.request()

def pump_working(q):
     #wait 10 sek until next break
      time.sleep(10)
      q.put("Broeken")
      
def work():      
     if __name__== '__main__':
        global queue_Asset_Working
        queue_Asset_Working=Queue()
        pump_work=Process(target=pump_working, args=(queue_Asset_Working,))
        pump_work.start()
def blink_service(gpio, queue, frequenz):
    #global qu
    #qu=Queue()
    pr=Process(target=activate_actor, args=(gpio,queue,frequenz))
    pr.start()

# count how many loop rounds asset is not on the RFID reader in variable asset_on_RFID
asset_on_RFID = 0
bulletin_activation=0
user_bulleting_deactivation=0

#work()
asset_broken = False
finished_working=False
bulette_fabrik_activated=False
bulette_fabrik_removed=False
user_informed_about_bulette=False

bulette_in=False

GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)


#endless loop
while True:
    #print bulletin_activation
    #print bulette_fabrik_activated


    if GPIO.input(SERVICE_BULETTE_CUSTOMER_MEASURRE)==1 and not user_informed_about_bulette and not asset_broken:
         print "New data from Service Bulette"
         user_informed_about_bulette=True
         time.sleep(2)
         GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.LOW)
         

    if GPIO.input(SERVICE_BULETTE_CUSTOMER_MEASURRE)==0 and user_informed_about_bulette and not asset_broken:
         #GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)
         user_informed_about_bulette=False
    


    #if user_informed_about_bulette and user_bulleting_deactivation>0:
     #    GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.LOW)


    #if GPIO.input(SERVICE_BULETTE_CUSTOMER_MEASURRE)==1:
     #    user_bulleting_deactivation=user_bulleting_deactivation+1
    

    
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
     
    if not asset_broken:
         (error, tag_type) = rdr.request()

    #if bulletin_activation>50 and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not bulette_fabrik_activated and not bulette_fabrik_removed and not asset_broken:
    if bulletin_activation>10 and not bulette_in and not bulette_fabrik_activated and not bulette_fabrik_removed and not asset_broken:
         bulette_fabrik_activated=True
         bulette_in=True
         global queue_bulette
         queue_bulette=Queue()
         blink_service(SERVICE_BULETTE, queue_bulette, 0.3)
         #GPIO.output(SERVICE_BULETTE, GPIO.HIGH)
         #bulletin_activation=0
         
    #if bulletin_activation<=50 and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not asset_broken:
    if bulletin_activation<=10 and not bulette_in and not asset_broken:
         #print str(bulletin_activation)
         bulletin_activation=bulletin_activation+1
         

    #if bulette_fabrik_activated==True and GPIO.input(SERVICE_BULETTE_FABRIK)==0 and not bulette_fabrik_removed and not asset_broken:
    if bulette_fabrik_activated==True and not bulette_in and not bulette_fabrik_removed and not asset_broken:
         #print "HAllo"
         bulette_fabrik_activated=False
         bulette_fabrik_removed=True
         GPIO.output(SERVICE_BULETTE_CUSTOMER, GPIO.HIGH)

    #if bulette_fabrik_activated==False and GPIO.input(SERVICE_BULETTE_FABRIK)==1 and bulette_fabrik_removed and not asset_broken:
    if bulette_fabrik_activated==False and bulette_in and bulette_fabrik_removed and not asset_broken:
         queue_bulette.put("Stop")
         bulette_in=False
         #GPIO.output(SERVICE_BULETTE, GPIO.LOW)
         #bulette_fabrik_activated=False
         bulette_fabrik_removed=False
         bulletin_activation=0

         
    #increase the round number only if the asset is not on the RFID reader several loop round in sequence (due to the RFID signal instability)
    if error and not asset_broken:
         asset_on_RFID=asset_on_RFID+1
    else:
         asset_on_RFID=0

    if GPIO.input(ASSET_BROCKEN)==1:
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

    if not asset_broken and finished_working:
         print "Asset is broken"
         asset_broken=True
         print "Repare the Asset!"
         asset_on_RFID=0
         #global qu
         qu=Queue()
         blink_service(OUT_service, qu, 0.5)
         finished_working=False
         
    if asset_broken:
          if GPIO.input(Pump)==1:
               asset_broken=False
               asset_on_RFID=0
               qu.put("Stop")
               #pr.terminate()
               #quequeue_Asset_Workingue=Queue()
               print "Congratulations, you repaired the Asset!"
               finished_working=False
               #work()
    
