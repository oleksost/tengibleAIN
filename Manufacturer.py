from Participant import Participant
from Bulette import Bulette
import datetime
import time
import RPi.GPIO as GPIO

class Manufacturer(Participant):
      """
      Manufacturer is a Participant, Manufacturer has additionaly a service Bullete to update his asset on the Operator's side
      """
      def __init__(self, gpio_out, service_bulleten_out=None, service_bullete_measure=None, bulette_at_campus=True, bulette=None):
        super(Manufacturer, self).__init__(gpio_out, service_bulleten_out, service_bullete_measure)
        self.Bulette=bulette
        self.Bulette_at_campus=bulette_at_campus
        #self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=10)
        self.Catalog={
        215:{'id':215 ,'type':'Pump','model':'1','price':1150, 'repairGPIO':38},
        138:{'id':138 ,'type':'Pump','model':'2','price':1500, 'repairGPIO':38},
        133:{'id':133 ,'type':'Pump','model':'3','price':2000, 'repairGPIO':38}
        }
        
        
      def activate_Bulette(self):
        self.Bulette.Activated=True
        self.blinker_Queue=Participant.blink_service(self.Service_Bulette_GPIO_out, 0.3)
        
      def deactivate_Bulette(self):
        self.Bulette.Activated=False
        Participant.stop_blink_service(self.blinker_Queue)
        self.set_next_asset_update_time()
      
      def set_next_asset_update_time(self):
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=10)
         
      def inform_operator_about_Update(self, operator):
         print "New data from Service Bulette"
         operator.Informed_about_recent_update=True
         self.set_next_asset_update_time()
         time.sleep(2)
         GPIO.output(operator.Service_Bulette_GPIO_out, GPIO.LOW)       
