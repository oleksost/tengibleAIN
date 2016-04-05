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
      def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None, bulletin_at_campus=True, bulletin=None, catalog=None):
        super(Manufacturer, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure, alarm_out)
        self.Bulletin=bulletin
        self.blinker_Queue=None
        self.Bulletin_at_campus=bulletin_at_campus
        self.Next_asset_update=0
        self.Catalog=catalog
        
      def activate_bulletin(self, main_gueue):
        self.blinker_Queue=Participant.blink_service(self.Service_Bulletin_GPIO_out, 0.3, main_gueue)
        
      def check_bulletin(self):
        if GPIO.input(self.Service_Bulletin_GPIO_Measure)==1:
          self.Bulletin_at_campus=False
        else:
          self.Bulletin_at_campus=True
        
      def deactivate_bulletin(self):
        if not self.blinker_Queue == None:
          Participant.stop_blink_service(self.blinker_Queue)

      
      def set_next_asset_update_time(self, seconds_=0):
        if seconds_==0:
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=random.randint(30, 30))
        else:
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=seconds_)
         
      def inform_operator_about_Update(self, operator):
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
         time.sleep(2)
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.LOW)
         self.set_next_asset_update_time()     
