from Participant import Participant
from Bulletin import Bulletin
import datetime
import time
import random
import RPi.GPIO as GPIO
from Webserver import WebSocketHandler

class Manufacturer(Participant):
      """
      Manufacturer is a Participant, Manufacturer has additionaly a service Bullete to update his asset on the Operator's side
      """
      def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None, bulletin_at_campus=True, bulletin=None):
        super(Manufacturer, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure)
        self.Bulletin=bulletin
        self.Bulletin_at_campus=bulletin_at_campus
        #self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=10)
        self.Catalog={
        215:{'id':215 ,'type':'Pump','model':'1','price':1150, 'repairGPIO':37},
        138:{'id':138 ,'type':'Pump','model':'2','price':1500, 'repairGPIO':37},
        133:{'id':133 ,'type':'Pump','model':'3','price':2000, 'repairGPIO':37}
        }
        
        
      def activate_bulletin(self, main_gueue):
        #self.Bulletin.Activated=True
        self.blinker_Queue=Participant.blink_service(self.Service_Bulletin_GPIO_out, 0.3, main_gueue)
        
      def check_bulletin(self):
        if GPIO.input(self.Service_Bulletin_GPIO_Measure)==1:
          self.Bulletin_at_campus=False
        else:
          self.Bulletin_at_campus=True
        
      def deactivate_bulletin(self):
        #self.Bulletin.Activated=False
        Participant.stop_blink_service(self.blinker_Queue)
        #self.set_next_asset_update_time()
      
      def set_next_asset_update_time(self):
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=random.randint(10, 20))
         
      def inform_operator_about_Update(self, operator):
         Participant.update_event(4)
         #WebSocketHandler.send_updates("New data from Service Bulletin")
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
         time.sleep(2)
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.LOW)
         #operator.Informed_about_recent_update=True
         self.set_next_asset_update_time()     
