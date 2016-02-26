import RPi.GPIO as GPIO
import RFID

class Asset(object):
      def __init__(self, rfid_identifier, name, gpio_in_to_repair, brocken):
        self.RFID_Identifier=rfid_identifier
        self.Name=name
        self.GPIO_to_repair=gpio_in_to_repair
        self.Brocken=brocken

