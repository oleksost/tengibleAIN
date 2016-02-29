import RPi.GPIO as GPIO
import random
import datetime

class Asset(object):
      def __init__(self, rfid_identifier, name, gpio_in_to_repair, brocken, last_break=datetime.datetime.now()):
        self.RFID_Identifier=rfid_identifier
        self.Name=name
        self.GPIO_to_repair=gpio_in_to_repair
        self.Brocken=brocken
        self.Last_Break=last_break
        self.Next_Break=last_break + datetime.timedelta(seconds=random.randint(20, 50))
        #print str(self.Next_Break)
        
        GPIO.setup(gpio_in_to_repair, GPIO.IN)


      def set_next_break(self):
        self.Last_Break=datetime.datetime.now()
        self.Next_Break=self.Last_Break + datetime.timedelta(seconds=random.randint(20, 50))