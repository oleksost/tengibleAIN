from Participant import Participant
from Manufacturer import Manufacturer
import time
import Pump
import __builtin__
import RFID 
import RPi.GPIO as GPIO
import datetime


class Operator(Participant):

     def __init__(self, gpio_out=None, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, informed_about_recent_update=False, pimp_gpio=None):
        super(Operator, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure, alarm_out)
        self.User_informed_about_recent_update=informed_about_recent_update
        self.Asset_not_on_RFID=on_RFID
        self.Has_asset=has_asset
        self.Blinker_queue_bulletin=None
        self.Asset=asset
        self.Asset_is_working=asset_works
        self.Pimp_GPIO=pimp_gpio
        ##sircuit security for service car handling
        self.service_car_at_operators=0
        if not pimp_gpio==None:
          GPIO.setup(pimp_gpio, GPIO.IN)


     def install_bulletin(self, manufacturer):
         GPIO.output(self.Service_Bulletin_GPIO_out, GPIO.HIGH)
         GPIO.output(manufacturer.GPIO_out, GPIO.HIGH)
         time.sleep(2)
         GPIO.output(self.Service_Bulletin_GPIO_out, GPIO.LOW)
         GPIO.output(manufacturer.GPIO_out, GPIO.LOW)
         manufacturer.set_next_asset_update_time()
          
     def buy_asset(self, manufacturer, main_queue, BREAK_ASSET_MANUALY_GPIO, service, GPIO_to_repair_for_demo):
        #global EMERGENCY
        if __builtin__.EMERGENCY:
            self.Asset=Operator.emergancy_asset(GPIO_to_repair_for_demo)
        else:
            self.Asset=Operator.readRFID(service, self,manufacturer.Catalog, main_queue, manufacturer, BREAK_ASSET_MANUALY_GPIO, main_queue, GPIO_to_repair_for_demo)
        print str(manufacturer.Bulletin_at_manufacturers_campus)
        self.Asset_is_working=True
        self.Asset_not_on_RFID=0
        #check if the asset is already boosted
        if GPIO.input(self.Pimp_GPIO)==0:
           self.Asset.Pimped=True
           
        Participant.asset_bought(self.Asset)
        #Participant.stop_blinking(blinker_Queue)
        GPIO.output(self.Service_Bulletin_GPIO_out, GPIO.LOW)
       
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
     def emergancy_asset(GPIO_to_repair_for_demo):
         Asset=Pump.Pump(rfid_identifier=215, gpio_in_to_repair=GPIO_to_repair_for_demo)
         return Asset


     @staticmethod
     def readRFID(service, operator, catalog, main_queue, manufacturer, BREAK_ASSET_MANUALY_GPIO, queue, GPIO_to_repair_for_demo):
       #global EMERGENCY
       broken_asset_security=0
       broken=False
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
         #Demonstrate the asset break even if there is no asset
         #print broken_asset_security
         if not broken:
           print broken_asset_security
           if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 0:
                    broken_asset_security = broken_asset_security + 1
           if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 1:
                    broken_asset_security = 0
         if broken_asset_security > 3:
                    broken_asset_security = 0
                    broken=True
                    Participant.handle_break(service, manufacturer, operator, queue)

         if broken:
           broken=Participant.handle_reparing(operator, service, manufacturer, GPIO_to_repair_for_demo)
           print broken
           if not broken:
               #to return to the event 0
               switch_to_event_0=datetime.datetime.now()+datetime.timedelta(seconds=10)
               event_updated=False

         if __builtin__.EMERGENCY:
            Asset=Operator.emergancy_asset(GPIO_to_repair_for_demo)
            operator.Has_asset=True
            break
            break

         if not switch_to_event_0==0:
          if datetime.datetime.now()>switch_to_event_0 and not event_updated and not broken:
            event_updated=True
            GPIO.output(manufacturer.GPIO_out, GPIO.LOW)
            GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
            Participant.update_event(0)
            manufacturer.Bulletin.Activated_for_communication=False
            operator.User_informed_about_recent_update=False
            switch_to_event_0=0
         (error, tag_type) = rdr.request()
         if not error and not broken:
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