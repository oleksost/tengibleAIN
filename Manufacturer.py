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
        self.Blinker_queue_bulletin=None
        #variable signaling that the bulletin is at the manufacturer's site
        self.Bulletin_at_manufacturers_campus=bulletin_at_campus
        self.Next_asset_update=0
        self.Catalog=catalog
        

        
      def check_bulletin(self):
        if GPIO.input(self.Service_Bulletin_GPIO_Measure)==1:
          self.Bulletin_at_campus=False
        else:
          self.Bulletin_at_campus=True

      
      def set_next_asset_update_time(self, seconds_=0):
        if seconds_==0:
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=random.randint(90, 90))
        else:
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=seconds_)
         
      def inform_operator_about_Update(self, operator):
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.HIGH) 
         time.sleep(2)
         GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.LOW)
         self.set_next_asset_update_time()

