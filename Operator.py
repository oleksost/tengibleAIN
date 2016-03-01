from Participant import Participant
import Pump
import RFID

class Operator(Participant):
     def __init__(self, gpio_out, service_bulleten_out=None, service_bullete_measure=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, informed_about_recent_update=False):
        super(Operator, self).__init__(gpio_out, service_bulleten_out, service_bullete_measure)
        self.Informed_about_recent_update=informed_about_recent_update
        self.asset_not_on_RFID=on_RFID 
        self.Has_asset=has_asset
        self.Asset=asset
        self.Asset_is_working=asset_works 
        
     def buy_asset(self, manufacturer):
        blinker_Queue=Participant.blink_service(self.GPIO_out,0.5)
        print "Operator: I need to buy a new pump!"
        #while not self.Has_asset:
        self.Asset=Operator.readRFID(self,manufacturer.Catalog)
        manufacturer.set_next_asset_update_time()
        self.Asset_is_working=True 
        self.asset_not_on_RFID=0
        self.Asset.set_next_break()
        
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
     def readRFID(operator, catalog):
       bought=False
       #global util
       global rdr
       rdr=RFID.RFID()
       Asset=None
       last_uid=0
       #util = rdr.util()
       while not operator.Has_asset:
        while True:
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