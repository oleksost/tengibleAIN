#!/usr/bin/python
import os
import tornado.httpserver
import __builtin__
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import multiprocessing
import threading
from Webserver import WebSocketHandler
from Webserver import MainHandler
import time
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
import signal

""" 
 EVENTS:
 #0 - initial setup
 #1 - no asset on rfid
 #2 - assert bought, asset information if sent to the frontend
 #3 - asset breaks
 #4 - inform user about the service bulletin functionality
 #5 - asset is repaired by the service car
 #6 - boost the asset
 #7 - unboost the asset
 #8 - 
 #9 - manufacturer wants to activate the bulletin
 #10 - remind to boost the asset
 #11 - remind to remove the service car form the manufacturer's facilities
 #12 - thanks for removing the car
 #14 - please put the bulletin to manufacturer for the activation
 #15 - emergency event
 
"""

# USE RPi.GPIO Layout (Pin-Numbers)
GPIO.setmode(GPIO.BOARD)
global ASSET_INSTALLED
#global EMERGENCY


def get_alife(Manufacturer_GPIO_out, Service_GPIO_out, Operator_GPIO_out,BREAK_ASSET_MANUALY_GPIO):
    #print str(Manufacturer_GPIO_out)
    #print str(Service_GPIO_out)
    #print str(Operator_GPIO_out)
    GPIO.output(Manufacturer_GPIO_out, GPIO.HIGH)
    GPIO.output(Service_GPIO_out, GPIO.HIGH)
    GPIO.output(Operator_GPIO_out, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(Manufacturer_GPIO_out, GPIO.LOW)
    GPIO.output(Service_GPIO_out, GPIO.LOW)
    GPIO.output(Operator_GPIO_out, GPIO.LOW)

    #checking if the participants' facilities are connected
    #for the operator:
    operator_connected_count = 0
    while operator_connected_count<10 and operator_connected_count>(-10):
        print operator_connected_count
        if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 0:
                    operator_connected_count =operator_connected_count+ 1
        if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 1:
                    operator_connected_count =operator_connected_count- 1
    if operator_connected_count>=10:
        __builtin__.operator_connected=False
    elif operator_connected_count<=-10:
        __builtin__.operator_connected=True


def main(a, queue):
    try:

        import multiprocessing
        import threading
        from Webserver import WebSocketHandler
        from Webserver import MainHandler
        from Participant import Participant
        from Bulletin import Bulletin
        from Operator import Operator
        from Service import Service
        from Manufacturer import Manufacturer
        import Pump
        import time
        import json
        import datetime
        import RPi.GPIO as GPIO
        from PIL import Image
        import pygame
        from multiprocessing import Process, Queue
        import signal
        from random import randint
        import RFID
        GPIO.setmode(GPIO.BOARD)

        # CONSTANTS
        PIMP_GPIO = 13 #gpio 27
        OUT_MANUFACTURER = 11 #gpio 17
        OUT_SERVICE = 33 #gpio 13
        ALARM_MANUFACTURER = 16 # gpio 23
        ALARM_OPERATOR = 7 #gpio 4
        ALARM_SERVICE = 38 #gpio 20
        REPAIR_ASSET_GPIO = 40 # gpio 21
        BREAK_ASSET_MANUALY_GPIO = 18 #gpio 24
        SERVICE_BULLETIN_MANUFACTURER = 31 #gpio 6v
        SERVICE_BULLETIN_MANUFACTURER_MEASURE = 35 #gpio 19
        SERVICE_BULLETIN_OPERATOR = 12 #gpio 18
        SERVICE_BULLETIN_OPERATOR_MEASURRE = 15 #gpio 22
        GPIO_to_repair_for_demo=40 # gpio 21

        # CATALOG OF RFID CHIPS' IDs THAT ARE ASSIGNED TO THE ASSETS IN THE FRONEND
        CATALOG = {
            215: {'id': 215, 'repairGPIO': REPAIR_ASSET_GPIO},
            216: {'id': 215, 'repairGPIO': REPAIR_ASSET_GPIO},
            98: {'id': 215, 'repairGPIO': REPAIR_ASSET_GPIO},
            209: {'id': 209, 'repairGPIO': REPAIR_ASSET_GPIO},
            133: {'id': 133, 'repairGPIO': REPAIR_ASSET_GPIO}
        }
        GPIO.setup(GPIO_to_repair_for_demo, GPIO.IN)
        # CREATING PARTICIPANTS OBJECTS
        Manufacturer = Manufacturer(OUT_MANUFACTURER, service_bulletin_out=SERVICE_BULLETIN_MANUFACTURER,
                                    service_bullete_measure=SERVICE_BULLETIN_MANUFACTURER_MEASURE,
                                    alarm_out=ALARM_MANUFACTURER, bulletin=Bulletin(), catalog=CATALOG)
        Service = Service(OUT_SERVICE, alarm_out=ALARM_SERVICE)
        Operator = Operator(service_bulletin_out=SERVICE_BULLETIN_OPERATOR,
                            service_bullete_measure=SERVICE_BULLETIN_OPERATOR_MEASURRE, alarm_out=ALARM_OPERATOR,
                            pimp_gpio=PIMP_GPIO)

        # SETTING ALL OUTPUTS TO LOW
        GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
        GPIO.output(Manufacturer.Service_Bulletin_GPIO_out, GPIO.LOW)
        GPIO.output(Manufacturer.ALARM_out, GPIO.LOW)
        GPIO.output(Operator.ALARM_out, GPIO.LOW)
        GPIO.output(Service.ALARM_out, GPIO.LOW)

        global ASSET_INSTALLED
        ASSET_INSTALLED = True
        #variable for the emergency handling, if the pump is not discovered
        #global EMERGENCY


        ############################

        ##SERVICE CAR HANDLING HELP-VARIABLES##
        #informed_to_remove_the_service_car = False

        ##################################

        GPIO.setup(BREAK_ASSET_MANUALY_GPIO, GPIO.IN)
        get_alife(Manufacturer.GPIO_out, Service.GPIO_out, Operator.Service_Bulletin_GPIO_out, BREAK_ASSET_MANUALY_GPIO)
        Participant.update_event(0)
        GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
        Operator.buy_asset(Manufacturer, queue, BREAK_ASSET_MANUALY_GPIO, Service, GPIO_to_repair_for_demo)

        while queue.empty():

            # CHECKING IF THE ASSET IS ON THE RFID READER
            if not __builtin__.EMERGENCY:
               Operator.check_asset()
            #for the emergency case
            if __builtin__.EMERGENCY and not __builtin__.operator_connected:
                Participant.update_event(15)

            # IF NO ASSET ON THE RFID READER00
            if not Operator.Has_asset and ASSET_INSTALLED:
                print "No Asset"
                if not Operator.User_informed_about_recent_update:
                    Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer = False
                Manufacturer.bulletin_stop_blinking()
                GPIO.output(SERVICE_BULLETIN_MANUFACTURER, GPIO.LOW)
                Manufacturer.Next_asset_update = 0
                GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                GPIO.output(Service.GPIO_out, GPIO.LOW)
                # ASSET_INSTALLED=False
                #Operator.Asset.Next_Pimp = 0
                Operator.Asset.Next_Break = 0
                GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                Participant.update_event(1)
                Operator.buy_asset(Manufacturer, queue, BREAK_ASSET_MANUALY_GPIO, Service, GPIO_to_repair_for_demo)

             ##BULLETIN HANDLING###
             #Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer=True when the bulletin has been activated by the manufacturer (first blinking after start)
             #Manufacturer.Bulletin.Activated_for_the_communication=True when the bulletin is installed on the operator's side for the first time
            if Operator.Has_asset and ASSET_INSTALLED and not Operator.Asset.Broken:
                #Next_asset_update is 0 only after the start of the demo
                if not Manufacturer.Next_asset_update == 0:
                    #one time bulletin activation at the manufacturer's site for the furthere communication
                    if datetime.datetime.now() > Manufacturer.Next_asset_update and not Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer and __builtin__.operator_connected:
                        GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                        if GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 0:
                            Participant.update_event(9)
                            print "setting blletin true"
                            Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer = True
                            Manufacturer.Bulletin_at_manufacturers_campus = True
                            Manufacturer.bulletin_start_blinking(queue)
                        else:
                            #inform user to put the service bulletin to the manufacturer's site first to load the agreements
                            Participant.update_event(14)

                else:
                    #first update over the service bulletin after the demo has started
                    Manufacturer.set_next_asset_update_time(22)

                #returning the activated bulletin to the manufacturer's site only causes the bulletin to blink signaling that it should be brought back to the operator's
                #if Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 0 and not Manufacturer.Bulletin_at_manufacturers_campus:
                 #   Manufacturer.bulletin_start_blinking(queue)
                  #  Manufacturer.Bulletin_at_manufacturers_campus = True
                    #Stoping blinking of the blue lamp at operator's site
                   # Operator.bulletin_stop_blinking()
                if Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 0 and __builtin__.operator_connected:
                    if not Manufacturer.Blinker_queue_bulletin.empty() or Manufacturer.Blinker_queue_bulletin==None:
                        Manufacturer.bulletin_start_blinking(queue)
                        Manufacturer.Bulletin_at_manufacturers_campus = True
                        if not Operator.Blinker_queue_bulletin==None and Operator.Blinker_queue_bulletin.empty:
                            Operator.bulletin_stop_blinking()
                            GPIO.output(SERVICE_BULLETIN_OPERATOR, GPIO.LOW)

                #The moment the bulleting is plugged of the manufacturer's site
                if Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer  and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 1 and Manufacturer.Bulletin_at_manufacturers_campus and __builtin__.operator_connected:
                    Manufacturer.bulletin_stop_blinking()
                    GPIO.output(SERVICE_BULLETIN_MANUFACTURER, GPIO.LOW)
                    GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                    Manufacturer.Bulletin_at_manufacturers_campus = False
                    #start blinking operator
                    Operator.bulletin_start_blinking(queue)

                if not Manufacturer.Next_asset_update == 0:
                    if Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer and GPIO.input(
                            Manufacturer.Service_Bulletin_GPIO_Measure) == 1 and GPIO.input(Operator.Service_Bulletin_GPIO_Measure)==0 and not Manufacturer.Bulletin_at_manufacturers_campus and __builtin__.operator_connected:
                      Manufacturer.Bulletin.Activated_for_the_communication=True
                      if Operator.Blinker_queue_bulletin.empty() and not Operator.Blinker_queue_bulletin is None:
                        #Stoping blinking of the blue lamp at operator's site
                        Operator.bulletin_stop_blinking()
                        GPIO.output(SERVICE_BULLETIN_OPERATOR, GPIO.LOW)
                      #when the service bulletin is intalled on the operator's site the updates are intalled periodically
                      if datetime.datetime.now() > Manufacturer.Next_asset_update:
                                print "Informing"
                                if not Operator.User_informed_about_recent_update:
                                    # Informing user about the service bulletin functionality only once at the beggining of the demo
                                    Participant.update_event(4)
                                    Operator.User_informed_about_recent_update = True
                                    # install bulletin first time
                                    Operator.bulletin_stop_blinking()
                                    GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
                                    time.sleep(4)
                                    GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
                                    Manufacturer.set_next_asset_update_time()
                                    #Operator.install_bulletin(Manufacturer)
                                    #Operator.Asset.set_next_break()
                                else:
                                    Manufacturer.inform_operator_about_Update(Operator)

            ##END BULLETIN HANDLING###


            # ASSET BREAK
              #MANUAL BREAK
                # can be issued by the presenter any time after the serice bulletin is installed by pressing the dedicated button
            if not Operator.Asset.Broken and __builtin__.operator_connected:
              #print Operator.Asset.broken_asset_security
              if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 0:
                     Operator.Asset.broken_asset_security = Operator.Asset.broken_asset_security + 1
              if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 1:
                     Operator.Asset.broken_asset_security = 0
              if Operator.Asset.broken_asset_security > 3:
                    Operator.Asset.broken_asset_security = 0
                    Operator.Asset_is_working = False
            #RANDOM BREAK - happens once when the power pack and pump are installed, bulletin is activated
            if Operator.Asset.Pimped and Operator.Has_asset and ASSET_INSTALLED and not Operator.Asset.Broken and Manufacturer.Bulletin.Activated_for_the_communication and __builtin__.operator_connected:
                # can happen only after the standard scenario is completed - after the booting part is installed
                if Operator.Asset.First_time_random_break:
                 if Operator.Asset.Next_Break == 0:
                    Operator.Asset.set_next_break()
                 if not Operator.Asset.Next_Break == 0:
                    if datetime.datetime.now() > Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Broken and Operator.Has_asset:
                        print "not working"
                        Operator.Asset.First_time_random_break=False
                        Operator.Asset_is_working = False

            if not Operator.Asset_is_working and not Operator.Asset.Broken and __builtin__.operator_connected:
                    Participant.handle_break(Service, Manufacturer, Operator, queue)
                    # END ASSET BREAK

            ##HANDLING THE SERVICE CAR AND REPAIRING THE ASSET#

            Participant.handle_reparing(Operator, Service, Manufacturer,GPIO_to_repair_for_demo)
            ### END HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##

            ####HANDLING ASSET BOOSTING
            if ASSET_INSTALLED and not Operator.Asset.Broken and Operator.Has_asset and __builtin__.operator_connected:
                print Operator.Asset.pimping
                if GPIO.input(Operator.Pimp_GPIO) == 0 and Operator.Asset.pimping < 5:
                    Operator.Asset.pimping += 1
                if GPIO.input(Operator.Pimp_GPIO) == 1 and Operator.Asset.pimping > 0:
                    Operator.Asset.pimping -= 1

                # remind to pimp the asset
                if not Manufacturer.Bulletin_at_manufacturers_campus and GPIO.input(
                        Operator.Service_Bulletin_GPIO_Measure) == 0 and not Operator.Asset.Pimped and Manufacturer.Bulletin.Activated_for_the_communication and Manufacturer.Bulletin.Agreement_loaded_on_bulletin_by_the_manufacturer:
                    if Operator.Asset.Next_Pimp == 0 and Manufacturer.Bulletin.Activated_for_the_communication:
                        # FIRST REMINDER
                        print "setting next pimp"
                        print str(Manufacturer.Bulletin.Activated_for_the_communication)
                        Operator.Asset.set_next_pimp_reminder(seconds_=8)
                    else:
                        if datetime.datetime.now() > Operator.Asset.Next_Pimp:
                            # REMINDER EVENT
                            print ("updating event 10")
                            Participant.update_event(10)
                            GPIO.output(Service.GPIO_out, GPIO.HIGH)
                            Operator.Asset.set_next_pimp_reminder()

                ##BOOSTING THE ASSET
                # if pimping>4 and not Operator.Asset.Pimped and not INFORMED_BULLETIN:
                if Operator.Asset.pimping == 5 and not Operator.Asset.Pimped:
                    Operator.pimp_the_pump()
                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
                    GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                    GPIO.output(Service.GPIO_out, GPIO.HIGH)
                    time.sleep(10)
                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
                    GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                    GPIO.output(Service.GPIO_out, GPIO.LOW)

                if Operator.Asset.pimping ==0 and Operator.Asset.Pimped and not Operator.Asset.Broken and Operator.Has_asset:
                    Operator.unpimp_the_pump(Service)
                    Operator.Asset.Next_Break = 0
                    Operator.Asset.set_next_pimp_reminder()

                    ##END BOOSTING THE ASSET
        print "stoped"

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when pressing CTRL+C
        GPIO.cleanup()
        http_server.stop()
        # except:
        # this catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working
        # print "Other error or exception occurred!"

    #finally:
        #GPIO.cleanup()  # this ensures a clean exit


# end main method



def check_ready_to_start():
    ready = True
    msg = ""
    return (ready, msg)


class StartHandler(tornado.web.RequestHandler):
    def get(self):
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        global Main_Queue
        global main_thread
        # print("button click")
        # check if everythings in place
        #(ready, msg) = check_ready_to_start()
        if threading.active_count() < 10:
            print "starting..."
            Main_Queue = Queue()
            main_thread = threading.Thread(target=main, args=(1, Main_Queue))
            main_thread.daemon = True
            main_thread.start()


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        print "Attempting to stop"
        try:
            Main_Queue.put("Stop")
            print str(threading.enumerate())

        except NameError:
            print "nothing to stop"

    def post(self):
        print "Attempting to stop"
        try:
            Main_Queue.put("Stop")
            print str(threading.enumerate())
        except NameError:
            print "nothing to stop"


class InstalledHandler(tornado.web.RequestHandler):
    def get(self):
        global ASSET_INSTALLED
        print "setting intalled"
        if ASSET_INSTALLED == False:
            ASSET_INSTALLED = True

    def post(self):
        print "setting intalled"
        global ASSET_INSTALLED
        if ASSET_INSTALLED == False:
            ASSET_INSTALLED = True

class EmergencyHandler(tornado.web.RequestHandler):
    def get(self):
        print "setting EMERGENCY"
        if __builtin__.EMERGENCY == False:
            __builtin__.EMERGENCY = True


    def post(self):

        print "setting EMERGENCY"
        if __builtin__.EMERGENCY == False:
            __builtin__.EMERGENCY = True


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/start/", StartHandler),
    (r"/stop/", StopHandler),
    #(r"/asset_installed/", InstalledHandler),
    (r"/emergency/", EmergencyHandler),
    # (r"/get_content_xml/", XMLLoader),
], debug=True, **settings)

if __name__ == "__main__":
    try:
        global ASSET_INSTALLED
        ASSET_INSTALLED = False
        __builtin__.EMERGENCY=False
        tornado.httpserver.HTTPServer.allow_reuse_address = True
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.allow_reuse_address = True
        http_server.listen(5000)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        # print"here is an interrupt 2"
        tornado.ioloop.IOLoop.instance().stop()
        http_server.stop()
        GPIO.cleanup()
        # except:
        # this catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working
        # print "Other error or exception occurred!"
        # http_server.stop()
        # GPIO.cleanup()

    finally:
        http_server.stop()
        GPIO.cleanup()
