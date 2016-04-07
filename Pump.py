import RPi.GPIO as GPIO
from Asset import Asset
import RFID

class Pump(Asset):
      def __init__(self, rfid_identifier=None, gpio_in_to_repair=None, broken=False, price=0, img=None, type="Unknown Pump", model="Unknown Model"):
        super(Pump, self).__init__(rfid_identifier, gpio_in_to_repair, broken, price)
        self.Pimped=False
        self.IMG=img
        self.Model=model
        self.Type=type
        
             
      """
      def pump_working(self, q):
        #wait 10 sek until next break
        time.sleep(10)
        q.put("Broeken")
      
      def work():      
        if __name__== '__main__':
          global queue_Asset_Working
          queue_Asset_Working=Queue()
          pump_work=Process(target=pump_working, args=(queue_Asset_Working,))
          pump_work.start()
      """ 
      