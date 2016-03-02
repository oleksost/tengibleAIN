#!/usr/bin/python
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

GPIO.setup(BREAK_ASSET, GPIO.IN)

Manufacturer=Manufacturer(OUT_manufacturer, SERVICE_BULETTE_FABRIK, SERVICE_BULETTE_FABRIK_MEASURE, bulletin=Bulletin())
Service=Service(OUT_service)
Operator=Operator(OUT_operator,SERVICE_BULETTE_CUSTOMER,SERVICE_BULETTE_CUSTOMER_MEASURRE)

def get_alife():
     GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
     GPIO.output(Service.GPIO_out, GPIO.HIGH)
     GPIO.output(Operator.GPIO_out, GPIO.HIGH)
     Participant.show_img("img/1.PNG")
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
    
get_alife()
#time.sleep(3)
#protection for multiprocessing, only for Windows
if __name__== '__main__':
     Operator.buy_asset(Manufacturer)
     
# count how many loop rounds asset is not on the RFID reader in variable asset_not_on_RFID  
asset_not_on_RFID = 0
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
         Manufacturer.activate_Bulletin()
         
    if Manufacturer.Bulletin.Activated and not bulletin_in and Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.Bulletin.Activated=False
         Manufacturer.Bulletin_at_campus=False
         GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)  

    if not Manufacturer.Bulletin.Activated and bulletin_in and not Manufacturer.Bulletin_at_campus and not Operator.Asset.Brocken:
         Manufacturer.deactivate_Bulletin()
         bulletin_in=False
         Manufacturer.Bulletin_at_campus=True
         
    #checking if the received the update from the Bulletin 
    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==1 and not Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Manufacturer.inform_operator_about_Update(Operator)
         #print "New data from Service Bulletin"
         #Operator.Informed_about_recent_update=True
         #Manufacturer.set_next_asset_update_time()
         #time.sleep(2)
         #GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)       

    if GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and Operator.Informed_about_recent_update and not Operator.Asset.Brocken:
         Operator.Informed_about_recent_update=False
         
    #manually break the asset
    if GPIO.input(BREAK_ASSET)==1:
         Operator.Asset_is_working=False
       
    if not Operator.Has_asset:
        print "No Asset"
        #Protection for multiprocessing, only for Windows
        if __name__== '__main__':
           Operator.buy_asset(Manufacturer)
           #Operator.Asset.set_next_break()   

    if not Operator.Asset.Brocken and not Operator.Asset_is_working:
         print "Asset is broken"
         Operator.Asset.Brocken=True
         Operator.asset_not_on_RFID=0
         print "Please, repare the Asset!"
     
         if __name__== '__main__':
           blinker_Queue=Service.blink_service(Service.GPIO_out,0.5)
         
    if Operator.Asset.Brocken and GPIO.input(Operator.Asset.GPIO_to_repair)==0:
               Service.repare_Asset(Operator,blinker_Queue)   
               
     #random asset break
    if datetime.datetime.now()>Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Brocken:
        Operator.Asset_is_working=False
        
    
