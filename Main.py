#!/usr/bin/python
from Participant import Participant
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

ASSET_UPDATE_FREQUENCY_OVER_SB=10

BREAK_ASSET=40
OUT_manufacturer=11
OUT_service=15
OUT_operator=12
SERVICE_BULETTE_FABRIK=31
SERVICE_BULETTE_FABRIK_MEASURE=33
SERVICE_BULETTE_CUSTOMER=16
SERVICE_BULETTE_CUSTOMER_MEASURRE=18


greating="Great choice! You just bought the Asset "
pygame.display.init()                 

GPIO.setup(BREAK_ASSET, GPIO.IN)

Manufacturer=Participant(OUT_manufacturer, SERVICE_BULETTE_FABRIK, SERVICE_BULETTE_FABRIK_MEASURE)
Service=Participant(OUT_service)
Operator=Participant(OUT_operator,SERVICE_BULETTE_CUSTOMER,SERVICE_BULETTE_CUSTOMER_MEASURRE)

def get_alife():
     GPIO.output(Manufacturer.OUT, GPIO.HIGH)
     GPIO.output(Service.OUT, GPIO.HIGH)
     GPIO.output(Operator.OUT, GPIO.HIGH)
     Participant.show_img("img/1.PNG")
     time.sleep(2)
     GPIO.output(Manufacturer.OUT, GPIO.LOW)
     GPIO.output(Service.OUT, GPIO.LOW)
     GPIO.output(Operator.OUT, GPIO.LOW)

def activate_actor(participant,q, frequenz):
    while q.empty():
      # LED an
      GPIO.output(participant, GPIO.HIGH)
      # Warte 100 ms
      time.sleep(frequenz)
      # LED aus
      GPIO.output(participant, GPIO.LOW)
      # Warte 100 ms
      time.sleep(frequenz)
def blink_service(gpio, queue, frequenz):
    pr=Process(target=activate_actor, args=(gpio,queue,frequenz))
    pr.start()

 #Calls GPIO cleanup
 #rdr.cleanup()  
          
get_alife()
time.sleep(3)
Operator.buy_asset()
 

    
def ckeck_if_info_bulette_in_place(GPIO_place):
   
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
         bulette_in=True
        
    else:
         bulette_in=False
    return bulette_in
   

# count how many loop rounds asset is not on the RFID reader in variable asset_not_on_RFID  
asset_not_on_RFID = 0
bulletin_activation=0

#work()

bulette_fabrik_activated=False
bulette_fabrik_removed=False
user_informed_about_bulette=False


GPIO.output(Operator.service_b_out, GPIO.HIGH)


#endless loop
while True:

    if GPIO.input(Operator.service_b_measure)==1 and not user_informed_about_bulette and not Operator.Asset.Brocken:
         print "New data from Service Bulette"
         user_informed_about_bulette=True
         time.sleep(2)
         GPIO.output(Operator.service_b_out, GPIO.LOW)       

    if GPIO.input(Operator.service_b_measure)==0 and user_informed_about_bulette and not Operator.Asset.Brocken:
         user_informed_about_bulette=False
    
    #check if Info Bulette in der Fabrik ist    
    bulette_in=ckeck_if_info_bulette_in_place(Manufacturer.service_b_measure)
    
    #checking if the Asset is on the RFID reader
    Operator.check_asset()

    if bulletin_activation>ASSET_UPDATE_FREQUENCY_OVER_SB and not bulette_in and not bulette_fabrik_activated and not bulette_fabrik_removed and not Operator.Asset.Brocken:
         bulette_fabrik_activated=True
         bulette_in=True
         global queue_bulette
         queue_bulette=Queue()
         blink_service(Manufacturer.service_b_out, queue_bulette, 0.3)
         
    if bulletin_activation<=ASSET_UPDATE_FREQUENCY_OVER_SB and not bulette_in and not Operator.Asset.Brocken:
         bulletin_activation=bulletin_activation+1
         
         
    if bulette_fabrik_activated==True and not bulette_in and not bulette_fabrik_removed and not Operator.Asset.Brocken:
         bulette_fabrik_activated=False
         bulette_fabrik_removed=True
         GPIO.output(Operator.service_b_out, GPIO.HIGH)

    if bulette_fabrik_activated==False and bulette_in and bulette_fabrik_removed and not Operator.Asset.Brocken:
         queue_bulette.put("Stop")
         bulette_in=False
         bulette_fabrik_removed=False
         bulletin_activation=0
        
    if GPIO.input(BREAK_ASSET)==1:
         Operator.Asset_is_working=False
     
       
    if not Operator.Has_asset:
        print "No Asset"
        Operator.buy_asset()
        #work()

    if not Operator.Asset.Brocken and not Operator.Asset_is_working:
         print "Asset is broken"
         Operator.Asset.Brocken=True
         Operator.asset_not_on_RFID=0
         print "Please, repare the Asset!"
     
         if __name__== '__main__':
           Service.blink_service(0.5)
  
         
    if Operator.Asset.Brocken:
          if GPIO.input(Operator.Asset.GPIO_to_repair)==1:
               Operator.Asset.Brocken=False
               Operator.asset_not_on_RFID=0
               Service.stop_blink_service()
               print "Congratulations, you repaired the Asset!"
               Operator.Asset_is_working=True
               #work()
    
