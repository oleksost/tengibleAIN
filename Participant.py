import time
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
#import pygame
import RFID
import Pump
import json
from Webserver import WebSocketHandler
GPIO.setmode(GPIO.BOARD)

class Participant(object):
    """
    class for the participants
    """
    #events
    operator_needs_asset=1
    operator_bought_asset=2
    operator_asset_brocken=3
    operator_infos_from_bulletin=4
    operator_asset_repared=5
    event_pimped_asset=6
    
    def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None):
        self.GPIO_out = gpio_out
        self.Service_Bulletin_GPIO_out = service_bulletin_out
        self.Service_Bulletin_GPIO_Measure = service_bullete_measure
        GPIO.setup(gpio_out, GPIO.OUT)
        if not service_bulletin_out==None and not service_bullete_measure== None:
          GPIO.setup(service_bulletin_out, GPIO.OUT)
          GPIO.setup(service_bullete_measure, GPIO.IN)
    @classmethod
    def update_event(cls, event, asset_rfid_id=0, hint_id=0):
       data = {}
       data['event'] = event
       data['asset_rfid_id'] = asset_rfid_id
       data['hint'] = hint_id
       json_data = json.dumps(data)
       WebSocketHandler.send_updates(json_data)
    
    @staticmethod
    def blink_service(out, frequenz, main_queue):
        qu=Queue()
        pr=Process(target=Participant.activate_actor, args=(out,qu,frequenz, main_queue))
        pr.daemon = True
        pr.start()
        return qu
        
    @staticmethod
    def stop_blink_service(qu):
          qu.put("Stop")
          
    @staticmethod
    def activate_actor(gpio, queue, frequenz, main_queue):
        while queue.empty() and main_queue.empty():
          # LED an
          GPIO.output(gpio, GPIO.HIGH)
          # Warte 100 ms
          time.sleep(frequenz)
          # LED aus
          GPIO.output(gpio, GPIO.LOW)
          # Warte 100 ms
          time.sleep(frequenz)
          
    @staticmethod
    def asset_bough(asset):
          #greating="Great choice! You just bought the Asset "
          Participant.update_event(2, asset.RFID_Identifier)
          #WebSocketHandler.send_updates(greating + "of Type: " + str(asset.Type)+", Model: "+str(asset.Model)+" Price: "+str(asset.Price))
          #Participant.show_img("img/2.PNG")
          time.sleep(1)
          #Participant.show_img("img/3.PNG")
          #time.sleep(1)

       
    @staticmethod
    def show_img(img):
       pygame.display.init()  
       imgSurf = pygame.image.load(img)
       imgSurf=pygame.transform.scale(imgSurf,(1280,1024))
       screen = pygame.display.set_mode(imgSurf.get_size())
       screen.blit (imgSurf,(0,0))
       pygame.display.flip()

