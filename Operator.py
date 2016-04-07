from Participant import Participant
from Manufacturer import Manufacturer
import time
import Pump
import RFID 
import RPi.GPIO as GPIO
import datetime


class Operator(Participant):
      
     def __init__(self, gpio_out=None, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, informed_about_recent_update=False, pimp_gpio=None):
        super(Operator, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure, alarm_out)
        self.User_informed_about_recent_update=informed_about_recent_update
        self.Asset_not_on_RFID=on_RFID
        self.Has_asset=has_asset
        self.Asset=asset
        self.Asset_is_working=asset_works
        self.Pimp_GPIO=pimp_gpio
        ##sircuit security for service car handling
        self.service_car_at_operators=0
        if not pimp_gpio==None:
          GPIO.setup(pimp_gpio, GPIO.IN)

     def inform_about_bulletin_functionality(self):
         Participant.update_event(4)
         self.User_informed_about_recent_update = True
         GPIO.output(self.Service_Bulletin_GPIO_out, GPIO.HIGH)
         time.sleep(2)
         GPIO.output(self.Service_Bulletin_GPIO_out, GPIO.LOW)
          
     def buy_asset(self, manufacturer, main_queue):
        self.Asset=Operator.readRFID(self,manufacturer.Catalog, main_queue, manufacturer)
        print str(manufacturer.Bulletin_at_manufacturers_campus)
        self.Asset_is_working=True 
        self.Asset_not_on_RFID=0
        #check if the asset is already boosted
        if GPIO.input(self.Pimp_GPIO)==0:
           self.Asset.Pimped=True
           
        Participant.asset_bough(self.Asset)
        #Participant.stop_blink_service(blinker_Queue)
        GPIO.output(self.ALARM_out, GPIO.LOW)
       
     def check_asset(self):
       (error, tag_type) = rdr.request()
       if error and not self.Asset.Broken:
           self.Asset_not_on_RFID += 1
       else:
           self.Asset_not_on_RFID=0
       
       if self.Asset_not_on_RFID>8 and self.Has_asset:
           self.Has_asset=False
           self.Asset_is_working=False     
     
     def pimp_the_pump(self):
        self.Asset.Pimped=True
        Participant.update_event(6, self.Asset.RFID_Identifier)
        #Participant.speak("Operator", "Successfully pimped the asset")
        
     def unpimp_the_pump(self, service):
        self.Asset.Pimped=False
        Participant.update_event(7, self.Asset.RFID_Identifier)
        GPIO.output(service.GPIO_out, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(service.GPIO_out, GPIO.LOW)
        #Participant.speak("Operator", "Unpimped the asset")    
     
     @staticmethod
     def readRFID(operator, catalog, main_queue, manufacturer):
       bought=False
       event_updated=False
       switch_to_event_0=datetime.datetime.now()+datetime.timedelta(seconds=10)
       #global util
       global rdr
       rdr=RFID.RFID()
       Asset=None
       last_uid=0
       #util = rdr.util()
       while not operator.Has_asset:
        while True and main_queue.empty():        
         if not switch_to_event_0==0:
          if datetime.datetime.now()>switch_to_event_0 and not event_updated:
           event_updated=True
           GPIO.output(manufacturer.GPIO_out, GPIO.LOW)
           GPIO.output(operator.ALARM_out, GPIO.HIGH)
           Participant.update_event(0)
           manufacturer.Bulletin.Activated_for_communication=False
           operator.User_informed_about_recent_update=False
           switch_to_event_0=0
         (error, tag_type) = rdr.request()    
         if not error:
           #print "Tag detected"
           (error, uid) = rdr.anticoll()
           if not error:
             #print "UID: " + str(uid[1])
             try:
                asset=catalog[uid[1]]
                Asset=Pump.Pump(rfid_identifier=asset['id'], gpio_in_to_repair=asset['repairGPIO'])
                GPIO.output(manufacturer.GPIO_out, GPIO.LOW)
                operator.Has_asset=True      
             except KeyError, e:
                if not uid[1]==last_uid:
                  print "The asset is not in the manufacturer's catalog, please try another asset"
                  last_uid=uid[1]
             break
       return Asset