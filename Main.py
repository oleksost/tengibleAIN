#!/usr/bin/python
from Participant import Participant
from Bulette import Bulette
from Operator import Operator
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

Manufacturer=Manufacturer	(OUT_manufacturer, SERVICE_BULETTE_FABRIK, SERVICE_BULETTE_FABRIK_MEASURE, bulette=Bulette())
Service=Participant(OUT_service)
Operator=Operator(OUT_operator,SERVICE_BULETTE_CUSTOMER,SERVICE_BULETTE_CUSTOMER_MEASURRE)

def get_alife():
     GPIO.output(Manufacturer.OUT, GPIO.HIGH)
     GPIO.output(Service.OUT, GPIO.HIGH)
     GPIO.output(Operator.OUT, GPIO.HIGH)
     Participant.show_img("img/1.PNG")
     time.sleep(2)
     GPIO.output(Manufacturer.OUT, GPIO.LOW)
     GPIO.output(Service.OUT, GPIO.LOW)
     GPIO.output(Operator.OUT, GPIO.LOW)

 #Calls GPIO cleanup
 #rdr.cleanup()  
          
get_alife()
time.sleep(3)

#protection for multiprocessing, only for Windows
if __name__== '__main__':
     Operator.buy_asset()
     Manufacturer.set_next_asset_update_time(Operator.Asset)
     
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

GPIO.output(Operator.service_b_out, GPIO.HIGH)

#endless loop
while True:

    #check if Info Bulette is plugged in the manufacturer, false by default and if not activated  
    bulette_in=ckeck_if_info_bulette_in_place(Manufacturer.service_b_measure)
    
    #checking if the Asset is on the RFID reader
    Operator.check_asset()

    if datetime.datetime.now()>Manufacturer.Next_asset_update and not bulette_in and not Manufacturer.Bulette.Activated and Manufacturer.Bulette_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulette.Activated=True
         bulette_in=True
         Manufacturer.activate_Bulette()
         
    if Manufacturer.Bulette.Activated and not bulette_in and Manufacturer.Bulette_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulette.Activated=False
         Manufacturer.Bulette_at_campus=False
         GPIO.output(Operator.service_b_out, GPIO.HIGH)  

    if not Manufacturer.Bulette.Activated and bulette_in and not Manufacturer.Bulette_at_campus and not Operator.Asset.Brocken:
         Manufacturer.deactivate_Bulette()
         bulette_in=False
         Manufacturer.Bulette_at_campus=True
    
    if GPIO.input(Operator.service_b_measure)==1 and not Operator.Imformed_about_recent_update and not Operator.Asset.Brocken:
         print "New data from Service Bulette"
         Operator.Imformed_about_recent_update=True
         Manufacturer.set_next_asset_update_time(Operator.Asset)
         time.sleep(2)
         GPIO.output(Operator.service_b_out, GPIO.LOW)       

    if GPIO.input(Operator.service_b_measure)==0 and Operator.Imformed_about_recent_update and not Operator.Asset.Brocken:
         Operator.Imformed_about_recent_update=False
         
    #manually break the asset
    if GPIO.input(BREAK_ASSET)==1:
         Operator.Asset_is_working=False
       
    if not Operator.Has_asset:
        print "No Asset"
        #Protection for multiprocessing, only for Windows
        if __name__== '__main__':
           Operator.buy_asset()
           Manufacturer.set_next_asset_update_time(Operator.Asset)
        #update the time for the next random break
        Operator.Asset.set_next_break()   

    if not Operator.Asset.Brocken and not Operator.Asset_is_working:
         print "Asset is broken"
         Operator.Asset.Brocken=True
         Operator.asset_not_on_RFID=0
         print "Please, repare the Asset!"
     
         if __name__== '__main__':
           blinker_Queue=Service.blink_service(Service.OUT,0.5)
         
    if Operator.Asset.Brocken:
          if GPIO.input(Operator.Asset.GPIO_to_repair)==1:
               Operator.Asset.Brocken=False
               Operator.asset_not_on_RFID=0
               Service.stop_blink_service(blinker_Queue)
               print "Congratulations, you repaired the Asset!"
               Operator.Asset_is_working=True
               #update the time for the next random break
               Operator.Asset.set_next_break()    
               
     #random asset break
    if datetime.datetime.now()>Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Brocken:
        Operator.Asset_is_working=False
        
    
