from Participant import Participant
import Pump
import RFID
import RPi.GPIO as GPIO


class Operator(Participant):
      
     def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, informed_about_recent_update=False, pimp_gpio=None):
        super(Operator, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure)
        self.Informed_about_recent_update=informed_about_recent_update
        self.Asset_not_on_RFID=on_RFID
        self.Has_asset=has_asset
        self.Asset=asset
        self.Asset_is_working=asset_works
        self.Pimp_GPIO=pimp_gpio
        if not pimp_gpio==None:
          GPIO.setup(pimp_gpio, GPIO.IN)
          
     def buy_asset(self, manufacturer, main_queue):
        blinker_Queue=Participant.blink_service(self.GPIO_out,0.5, main_queue)
        Participant.update_event(1)
        #Participant.speak("Operator", "I need to buy a new pump!")
        #print "Operator: I need to buy a new pump!"
        #while not self.Has_asset:
        self.Asset=Operator.readRFID(self,manufacturer.Catalog, main_queue)
        manufacturer.set_next_asset_update_time()
        print("nxt update time is set")
        print str(manufacturer.Bulletin_at_campus)
        manufacturer.check_bulletin()
        #print str(manufacturer.Service_Bulletin_GPIO_Measure)
        #print str(manufacturer.Bulletin_at_campus)
        if not manufacturer.Bulletin_at_campus and not manufacturer.Bulletin.Activated:
            #Participant.update_event(8)
            print("To receive new updates verify the bulletin at manufacturers")
        
        self.Asset_is_working=True 
        self.Asset_not_on_RFID=0
        self.Asset.set_next_break()
        
        Participant.asset_bough(self.Asset)
        Participant.stop_blink_service(blinker_Queue)
        #Participant.show_img("img/1.PNG")
       
     def check_asset(self):
       (error, tag_type) = rdr.request()
       if error and not self.Asset.Brocken:
           self.Asset_not_on_RFID += 1
       else:
           self.Asset_not_on_RFID=0
       
       if self.Asset_not_on_RFID>2 and self.Has_asset:
           self.Has_asset=False
           self.Asset_is_working=False     
     
     def pimp_the_pump(self):
        self.Asset.Pimped=True
        Participant.update_event(6)
        #Participant.speak("Operator", "Successfully pimped the asset")
      
     def unpimp_the_pump(self):
        self.Asset.Pimped=False
        Participant.update_event(7)
        #Participant.speak("Operator", "Unpimped the asset")    
           
     @staticmethod
     def readRFID(operator, catalog, main_queue):
       bought=False
       #global util
       global rdr
       rdr=RFID.RFID()
       Asset=None
       last_uid=0
       #util = rdr.util()
       while not operator.Has_asset:
        while True and main_queue.empty():
         (error, tag_type) = rdr.request()
         if not error:
           #print "Tag detected"
           (error, uid) = rdr.anticoll()
           if not error:
             #print "UID: " + str(uid[1])
             try:
                asset=catalog[uid[1]]
                Asset=Pump.Pump(rfid_identifier=asset['id'], gpio_in_to_repair=asset['repairGPIO'], price=asset['price'], type=asset['type'], model=asset['model'])
                operator.Has_asset=True      
             except KeyError, e:
                if not uid[1]==last_uid:
                  print "The asset is not in the manufacturer's catalog, please try another asset"
                  last_uid=uid[1]
             break
           
          
       return Asset