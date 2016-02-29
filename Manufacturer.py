from Participant import Participant
from Bulette import Bulette
import datetime

class Manufacturer(Participant):
      """
      Manufacturer is a Participant, Manufacturer has additionaly a service Bullete to update his asset on the Operator's side
      """
      def __init__(self, gpio_out, service_bulleten_out=None, service_bullete_measure=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, bulette_at_campus=True, bulette=None):
        super(Manufacturer, self).__init__(gpio_out, service_bulleten_out, service_bullete_measure, has_asset, asset, asset_works, on_RFID)
        self.Bulette=bulette
        self.Bulette_at_campus=bulette_at_campus
        #self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=10)
        if has_asset==False:
           self.Next_asset_update=None
        
      def activate_Bulette(self):
        self.Bulette.Activated=True
        self.blinker_Queue=Participant.blink_service(self.service_b_out, 0.3)
        
      def deactivate_Bulette(self):
        self.Bulette.Activated=False
        Participant.stop_blink_service(self.blinker_Queue)
        self.set_next_asset_update_time(self.Asset)
      
      def set_next_asset_update_time(self, Asset):
         self.Next_asset_update=datetime.datetime.now()+datetime.timedelta(seconds=10)