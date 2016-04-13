import time
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
#import pygame
import RFID
import Pump
import json
import datetime
from Webserver import WebSocketHandler
GPIO.setmode(GPIO.BOARD)

class Participant(object):
        """
        class for the participants
        """
        #events
        informed_to_remove_the_service_car=False


        def __init__(self, gpio_out=None, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None, blinker_queue=None):
                self.GPIO_out = gpio_out
                self.Blinker_queue=blinker_queue
                self.ALARM_out=alarm_out
                self.Service_Bulletin_GPIO_out = service_bulletin_out
                self.Service_Bulletin_GPIO_Measure = service_bullete_measure
                if not alarm_out==None:
                          GPIO.setup(alarm_out, GPIO.OUT)
                if not gpio_out==None:
                          GPIO.setup(gpio_out, GPIO.OUT)
                if not service_bulletin_out==None and not service_bullete_measure== None:
                  GPIO.setup(service_bulletin_out, GPIO.OUT)
                  GPIO.setup(service_bullete_measure, GPIO.IN)

        def bulletin_start_blinking(self, main_queue):
              self.Blinker_queue_bulletin=Participant.blink_bulletin(self.Service_Bulletin_GPIO_out, 0.3, main_queue)

        def bulletin_stop_blinking(self):
             if not self.Blinker_queue_bulletin == None:
                  Participant.stop_blinking(self.Blinker_queue_bulletin)

        @classmethod
        def update_event(cls, event, asset_rfid_id=0, pimped=False):
           data = {}
           data['event'] = event
           data['asset_rfid_id'] = asset_rfid_id
           data['pimped'] = pimped
           json_data = json.dumps(data)
           WebSocketHandler.send_updates(json_data)

        @staticmethod
        def blink_alarm(participant, frequenz, main_queue):
            blinker_queue=Queue()
            pr=Process(target=Participant.activate_actor, args=(participant.ALARM_out,blinker_queue,frequenz, main_queue))
            pr.daemon = True
            pr.start()
            participant.Blinker_queue=blinker_queue

        @staticmethod
        def handle_break(service, manufacturer, operator, queue):
            Participant.update_event(3)
            if not operator.Asset is None:
               operator.Asset.Broken = True
               #operator.Asset.set_next_pimp_reminder(seconds_=8)
            operator.Asset_not_on_RFID = 0
            # If the boost reminder had been issued right before the asset break
            GPIO.output(service.GPIO_out, GPIO.LOW)
            #turn off lights in case its on
            GPIO.output(manufacturer.GPIO_out, GPIO.LOW)
            GPIO.output(operator.Service_Bulletin_GPIO_out, GPIO.LOW)
            #stop bulletin blining in case it is blinking
            manufacturer.bulletin_stop_blinking()
            # Blink alarm all
            Participant.blink_alarm(service, 0.5, queue)
            Participant.blink_alarm(operator, 0.5, queue)
            Participant.blink_alarm(manufacturer, 0.5, queue)

        @staticmethod
        def blink_bulletin(out, frequenz, main_queue):
            blinker_queue=Queue()
            pr=Process(target=Participant.activate_actor, args=(out,blinker_queue,frequenz, main_queue))
            pr.daemon = True
            pr.start()
            return blinker_queue

        @staticmethod
        def stop_blinking(participant_queue):
            if not participant_queue is None:
              participant_queue.put("Stop")


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
        def asset_bought(asset):
              #greating="Great choice! You just bought the Asset"
              if asset.Pimped:
               Participant.update_event(2, asset.RFID_Identifier, True)
              else:
               Participant.update_event(2, asset.RFID_Identifier)

        @staticmethod
        def handle_reparing(Operator, Service, Manufacturer , GPIO_to_repair_for_demo):
              broken=True
              if not Operator.Asset is None:
                if GPIO.input(Operator.Asset.GPIO_to_repair) == 0 and Operator.service_car_at_operators <= 2:
                    Operator.service_car_at_operators += 1
                if GPIO.input(Operator.Asset.GPIO_to_repair) == 1:
                    Operator.service_car_at_operators = 0

                # check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
                if Operator.Asset.Broken and Operator.service_car_at_operators > 1:
                    # stops blinking ALL
                    Service.repare_Asset(Operator, Service, Manufacturer)
                    Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=10)
                    Participant.informed_to_remove_the_service_car = False
                    Manufacturer.set_next_asset_update_time(10)
                    broken=False
                if not Service.next_hint_to_return_the_serive_car == 0:
                    if not Operator.Asset.Broken and Operator.service_car_at_operators > 1 and datetime.datetime.now() > Service.next_hint_to_return_the_serive_car:
                        # hint: place the service car back to the service station
                        Participant.update_event(11)
                        GPIO.output(Service.GPIO_out, GPIO.HIGH)
                        Participant.informed_to_remove_the_service_car = True
                        Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=20)
              else:
                if GPIO.input(GPIO_to_repair_for_demo) == 0 and Operator.service_car_at_operators <= 2:
                    Operator.service_car_at_operators += 1
                if GPIO.input(GPIO_to_repair_for_demo) == 1:
                    Operator.service_car_at_operators = 0

                # check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
                if Operator.service_car_at_operators > 1:
                    # stops blinking ALL
                    Service.repare_Asset(Operator, Service, Manufacturer)
                    #Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=10)
                    Participant.informed_to_remove_the_service_car = False
                    broken=False
                if not Service.next_hint_to_return_the_serive_car == 0:
                    if Operator.service_car_at_operators > 1 and datetime.datetime.now() > Service.next_hint_to_return_the_serive_car:
                        # hint: place the service car back to the service station
                        Participant.update_event(11)
                        GPIO.output(Service.GPIO_out, GPIO.HIGH)
                        Participant.informed_to_remove_the_service_car = True
                        Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=20)
              if Operator.service_car_at_operators == 0:
                    Service.next_hint_to_return_the_serive_car = 0
                    if Participant.informed_to_remove_the_service_car:
                        Participant.update_event(12)
                        GPIO.output(Service.GPIO_out, GPIO.LOW)
                        Participant.informed_to_remove_the_service_car = False

              return broken