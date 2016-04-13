import RPi.GPIO as GPIO
import random
import datetime

class Asset(object):
      def __init__(self, rfid_identifier, gpio_in_to_repair, broken, first_time_random_break=True):
        self.RFID_Identifier=rfid_identifier
        self.GPIO_to_repair=gpio_in_to_repair
        self.Broken=broken
        self.Next_Break=0
        self.Next_Pimp=0
        #sircuit security for asset boosting
        self.pimping = 0
        #asset breaks once after pump and power pack have been installed and the bulletin activated for the communication
        self.First_time_random_break=first_time_random_break
        #sircuit security for asset break
        self.broken_asset_security=0
        #GPIO.setup(gpio_in_to_repair, GPIO.IN)


      def set_next_break(self):
        print "Set next break"
        self.Next_Break=datetime.datetime.now() + datetime.timedelta(seconds=60)
        
      def set_next_pimp_reminder(self, seconds_=0):
       if seconds_==0:
        self.Next_Pimp=datetime.datetime.now() + datetime.timedelta(seconds=random.randint(60, 60))
       else:
        self.Next_Pimp=datetime.datetime.now() + datetime.timedelta(seconds=seconds_)