import time
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import pygame
import RFID
import Pump

class Participant(object):
    """
    class for the participants
    """
    
    def __init__(self, gpio_out, service_bulleten_out=None, service_bullete_measure=None, has_asset=False, asset=None, asset_works=False, on_RFID=0):
        self.OUT = gpio_out
        self.service_b_out = service_bulleten_out
        self.service_b_measure = service_bullete_measure
        self.Has_asset=has_asset
        #asset_not_on_RFID - helper variable for the tracking if the asset is on the RFID reader
        self.asset_not_on_RFID=on_RFID  
        GPIO.setup(gpio_out, GPIO.OUT)
        self.Asset=asset
        self.Asset_is_working=asset_works
        
        if not service_bulleten_out==None and not service_bullete_measure== None:
          GPIO.setup(service_bulleten_out, GPIO.OUT)
          GPIO.setup(service_bullete_measure, GPIO.IN)
     


 
    def buy_asset(self):
       blinker_Queue=Participant.blink_service(self.OUT,0.5)
       print "Operator: I need to buy a new pump!"
       self.Asset=Participant.readRFID()
       self.Has_asset=True
       self.Asset_is_working=True 
       self.asset_not_on_RFID=0
       Participant.asset_bough(self.Asset)
       Participant.stop_blink_service(blinker_Queue)
       Participant.show_img("img/1.PNG")
      
    def check_asset(self):
       (error, tag_type) = rdr.request()
       if error and not self.Asset.Brocken:
           self.asset_not_on_RFID += 1
       else:
           self.asset_not_on_RFID=0
       
       if self.asset_not_on_RFID>2 and self.Has_asset:
           self.Has_asset=False
           self.Asset_is_working=False
           


    
    @staticmethod
    def blink_service(out, frequenz):
        qu=Queue()
        pr=Process(target=Participant.activate_actor, args=(out,qu,frequenz))
        pr.start()
        return qu
        
    @staticmethod
    def stop_blink_service(qu):
          qu.put("Stop")
          
    @staticmethod
    def activate_actor(gpio, q, frequenz):
        while q.empty():
          # LED an
          GPIO.output(gpio, GPIO.HIGH)
          # Warte 100 ms
          time.sleep(frequenz)
          # LED aus
          GPIO.output(gpio, GPIO.LOW)
          # Warte 100 ms
          time.sleep(frequenz)
          
    @staticmethod
    def asset_bough(asset):
          greating="Great choice! You just bought the Asset "
          print greating + str(asset.Name)
          Participant.show_img("img/2.PNG")
          time.sleep(3)
          Participant.show_img("img/3.PNG")
          time.sleep(3)

    @staticmethod
    def readRFID():
       ASSET_1 = 38
       ASSET_2 = 38
       ASSET_3 = 38 
       bought=False
       #global util
       global rdr
       rdr=RFID.RFID()
       #util = rdr.util()
       while True:
         (error, tag_type) = rdr.request()
         if not error:
           #print "Tag detected"
           (error, uid) = rdr.anticoll()
           if not error:
             #print "UID: " + str(uid[1])
             if uid[1]==215:
               Asset=Pump.Pump(uid[1], "Pump 1", ASSET_1, False, None)
               break
             if uid[1]==138:
               Asset=Pump.Pump(uid[1], "Pump 2", ASSET_2, False, None)
               break
             if uid[1]==133:
               Asset=Pump.Pump(uid[1], "Pump 3", ASSET_3, False, None)
               break
       return Asset
    
    @staticmethod
    def show_img(img):
       pygame.display.init()  
       imgSurf = pygame.image.load(img)
       imgSurf=pygame.transform.scale(imgSurf,(1280,1024))
       screen = pygame.display.set_mode(imgSurf.get_size())
       screen.blit (imgSurf,(0,0))
       pygame.display.flip()

