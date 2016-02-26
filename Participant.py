import time
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue

class Participant:
    """
    class for the participants
    """
        
    def __init__(self, gpio_out):
        self.OUT = gpio_out
        GPIO.setup(gpio_out, GPIO.OUT)

    def blink_service(self,frequenz):
        global qu
        qu=Queue()
        pr=Process(target=self.activate_actor, args=(self.OUT,qu,frequenz))
        pr.start()
        
    def stop_blink_service(self):
          qu.put("Stop")
          
    @staticmethod
    def activate_actor(gpio, q, frequenz):
        while q.empty():
          # LED an
          GPIO.output(gpio, GPIO.HIGH)
          # Warte 100 ms
          time.sleep(frequenz)
          # LED aus
          GPIO.output(gpio, GPIO.LOW)
          # Warte 100 ms
          time.sleep(frequenz)
    
    
        


