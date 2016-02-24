import time
import RPi.GPIO as GPIO

class Participant(object):
    """
    abstract class for the participants
    """
     def __init__(self, gpio_out):
        self.GPIO_OUT = gpio_out

     def blink_service(gpio, queue, frequenz):
        #global qu
        #qu=Queue()
        pr=Process(target=activate_actor, args=(gpio,queue,frequenz))
        pr.start()

     def activate_actor(actor,q, frequenz):

        while q.empty():
          # LED an
          GPIO.output(actor, GPIO.HIGH)
          # Warte 100 ms
          time.sleep(frequenz)
          # LED aus
          GPIO.output(actor, GPIO.LOW)
          # Warte 100 ms
          time.sleep(frequenz)


