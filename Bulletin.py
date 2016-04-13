
class Bulletin(object):
     def __init__(self, Update_Information="Planned maintanance", agrreement_loaded=False, activated=False, blinker_queue=None):
         #Agreement_loaded_on_bulletin_by_the_manufacturer=True when the bulletin has been activated by the manufacturer (first blinking after start)
         #Activated_for_the_communication=True when the bulletin is installed on the operator's side for the first time
         self.Update_Information=Update_Information
         self.Blinker_queue=blinker_queue
         self.Agreement_loaded_on_bulletin_by_the_manufacturer=agrreement_loaded
         self.Activated_for_the_communication=activated
     
     
     
     
        