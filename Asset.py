import RPi.GPIO as GPIO
import random
import datetime

class Asset(object):
      def __init__(self, rfid_identifier, gpio_in_to_repair, broken, price):
        self.RFID_Identifier=rfid_identifier
        self.Price=price
        self.GPIO_to_repair=gpio_in_to_repair
        self.Broken=broken
        self.Next_Break=0
        self.Next_Pimp=0
        #sircuit security for asset boosting
        self.pimping = 0
        #sircuit security for asset break
        self.broken_asset_security=0
        GPIO.setup(gpio_in_to_repair, GPIO.IN)


      def set_next_break(self):
        print "Set next break"
        self.Next_Break=datetime.datetime.now() + datetime.timedelta(seconds=60)
        
      def set_next_pimp_reminder(self, seconds_=0):
       if seconds_==0:
        self.Next_Pimp=datetime.datetime.now() + datetime.timedelta(seconds=random.randint(60, 60))
       else:
        self.Next_Pimp=datetime.datetime.now() + datetime.timedelta(seconds=seconds_)