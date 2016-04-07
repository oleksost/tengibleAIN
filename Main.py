#!/usr/bin/python
import os
import tornado.httpserver
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
 #9 - manufacturer wants to activat the bulletin
 #10 - remind to boost the asset
 #11 - remind to remove the service car form the manufacturer's facilities
 #12 - thanks for removing the car
 
"""

# USE RPi.GPIO Layout (Pin-Numbers)
GPIO.setmode(GPIO.BOARD)
global ASSET_INSTALLED


def get_alife(Manufacturer_GPIO_out, Service_GPIO_out, Operator_GPIO_out):
    print str(Manufacturer_GPIO_out)
    print str(Service_GPIO_out)
    print str(Operator_GPIO_out)
    GPIO.output(Manufacturer_GPIO_out, GPIO.HIGH)
    GPIO.output(Service_GPIO_out, GPIO.HIGH)
    GPIO.output(Operator_GPIO_out, GPIO.HIGH)
    # Participant.show_img("img/1.PNG")
    time.sleep(2)
    GPIO.output(Manufacturer_GPIO_out, GPIO.LOW)
    GPIO.output(Service_GPIO_out, GPIO.LOW)
    GPIO.output(Operator_GPIO_out, GPIO.LOW)


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
        PIMP_GPIO = 7
        OUT_MANUFACTURER = 11
        OUT_SERVICE = 15
        ALARM_MANUFACTURER = 16
        ALARM_OPERATOR = 12
        ALARM_SERVICE = 38
        REPAIR_ASSET_GPIO = 13
        BREAK_ASSET_MANUALY_GPIO = 40
        SERVICE_BULETTE_MANUFACTURER = 31
        SERVICE_BULETTE_MANUFACTURER_MEASURE = 35
        SERVICE_BULETTE_OPERATOR = 29
        SERVICE_BULETTE_OPERATOR_MEASURRE = 33

        # CATALOG OF RFID CHIPS' IDs THAT ARE ASSIGNED TO THE ASSETS IN THE FRONEND
        CATALOG = {
            215: {'id': 215, 'repairGPIO': REPAIR_ASSET_GPIO},
            98: {'id': 215, 'repairGPIO': REPAIR_ASSET_GPIO},
            209: {'id': 209, 'repairGPIO': REPAIR_ASSET_GPIO},
            133: {'id': 133, 'repairGPIO': REPAIR_ASSET_GPIO}
        }
        # CREATING PARTICIPANTS OBJECTS
        Manufacturer = Manufacturer(OUT_MANUFACTURER, service_bulletin_out=SERVICE_BULETTE_MANUFACTURER,
                                    service_bullete_measure=SERVICE_BULETTE_MANUFACTURER_MEASURE,
                                    alarm_out=ALARM_MANUFACTURER, bulletin=Bulletin(), catalog=CATALOG)
        Service = Service(OUT_SERVICE, alarm_out=ALARM_SERVICE)
        Operator = Operator(service_bulletin_out=SERVICE_BULETTE_OPERATOR,
                            service_bullete_measure=SERVICE_BULETTE_OPERATOR_MEASURRE, alarm_out=ALARM_OPERATOR,
                            pimp_gpio=PIMP_GPIO)

        # SETTING ALL OUTPUTS TO LOW
        GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
        GPIO.output(Manufacturer.Service_Bulletin_GPIO_out, GPIO.LOW)
        GPIO.output(Manufacturer.ALARM_out, GPIO.LOW)
        GPIO.output(Operator.ALARM_out, GPIO.LOW)
        GPIO.output(Service.ALARM_out, GPIO.LOW)

        global ASSET_INSTALLED
        ASSET_INSTALLED = True


        ############################

        ##SERVICE CAR HANDLING VARIABLES##
        informed_to_remove_the_service_car = False

        ##################################

        GPIO.setup(BREAK_ASSET_MANUALY_GPIO, GPIO.IN)
        get_alife(Manufacturer.GPIO_out, Service.GPIO_out, Operator.Service_Bulletin_GPIO_out)
        Participant.update_event(0)
        GPIO.output(Operator.ALARM_out, GPIO.HIGH)
        Operator.buy_asset(Manufacturer, queue)

        while queue.empty():

            # CHECKING IF THE ASSET IS ON THE RFID READER
            Operator.check_asset()

            # IF NOT OPERATOR ON THE RFID CREADER
            if not Operator.Has_asset and ASSET_INSTALLED:
                print "No Asset"
                if not Operator.User_informed_about_recent_update:
                    Manufacturer.Bulletin.Activated_for_communication = False
                Manufacturer.debulletin_start_blinking()
                Manufacturer.Next_asset_update = 0
                GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                GPIO.output(Service.GPIO_out, GPIO.LOW)
                # ASSET_INSTALLED=False
                Operator.Asset.Next_Pimp = 0
                Operator.Asset.Next_Break = 0
                GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                Participant.update_event(1)
                Operator.buy_asset(Manufacturer, queue)

                ##BULLETIN HANDLING###
            if Operator.Has_asset and ASSET_INSTALLED and not Operator.Asset.Broken and Operator.Has_asset:
                #Next_asset_update is 0 only after the demo start
                if not Manufacturer.Next_asset_update == 0:
                    #one time bulletin activation at the manufacturer's site for the furthere communication
                    if datetime.datetime.now() > Manufacturer.Next_asset_update and not Manufacturer.Bulletin.Activated_for_communication:
                        Participant.update_event(9)
                        GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                        if GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 0:
                            Manufacturer.Bulletin.Activated_for_communication = True
                            Manufacturer.Bulletin_at_manufacturers_campus = True
                            Manufacturer.bulletin_start_blinking(queue)
                else:
                    #first update over the service bulletin after the demo start is set
                    Manufacturer.set_next_asset_update_time(22)
                #returning the activated bulletin to the manufacturer's site only causes the bulletin to blink signaling that it should be brought back to the operator's
                if Manufacturer.Bulletin.Activated_for_communication and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 0 and not Manufacturer.Bulletin_at_manufacturers_campus:
                    Manufacturer.bulletin_start_blinking(queue)
                    Manufacturer.Bulletin_at_manufacturers_campus = True
                #The moment the bulleting is plugged of the manufacturer's site
                if Manufacturer.Bulletin.Activated_for_communication and GPIO.input(Manufacturer.Service_Bulletin_GPIO_Measure) == 1 and Manufacturer.Bulletin_at_manufacturers_campus:
                    Manufacturer.bulletin_stop_blinking()
                    GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                    Manufacturer.Bulletin_at_manufacturers_campus = False

                if not Manufacturer.Next_asset_update == 0:
                    #when the service bulletin is intalled on the operator's site the updates are intalled periodically
                    if datetime.datetime.now() > Manufacturer.Next_asset_update and GPIO.input(
                            Operator.Service_Bulletin_GPIO_Measure) == 0 and Manufacturer.Bulletin.Activated_for_communication and GPIO.input(
                            Manufacturer.Service_Bulletin_GPIO_Measure) == 1 and not Manufacturer.Bulletin_at_manufacturers_campus:
                        print "Informing"
                        Manufacturer.inform_operator_about_Update(Operator)
                        # Informing user about the service bulletin functionality only once at the beggining of the demo
                        if not Operator.User_informed_about_recent_update:
                            Operator.inform_about_bulletin_functionality()
            ##END BULLETIN HANDLING###


            # ASSET BREAK
            if Operator.Has_asset and ASSET_INSTALLED and not Operator.Asset.Broken and Manufacturer.Bulletin.Activated_for_communication:
                #MANUAL BREAK
                # can be issued by the presenter any time after the serice bulletin is installed by pressing the dedicated button
                print Operator.Asset.broken_asset_security
                if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 1:
                    Operator.Asset.broken_asset_security = Operator.Asset.broken_asset_security + 1
                if GPIO.input(BREAK_ASSET_MANUALY_GPIO) == 0:
                    Operator.Asset.broken_asset_security = 0
                if Operator.Asset.broken_asset_security > 5:
                    Operator.Asset_is_working = False
                    Operator.Asset.broken_asset_security = 0

                #RANDOM BREAK
                # can happen only after the standard scenario is completed - after the booting part is installed
                if Operator.Asset.Next_Break == 0 and Operator.Asset.Pimped:
                    Operator.Asset.set_next_break()
                if not Operator.Asset.Next_Break == 0:
                    if datetime.datetime.now() > Operator.Asset.Next_Break and Operator.Asset_is_working and not Operator.Asset.Broken and Operator.Has_asset:
                        print "not working"
                        Operator.Asset_is_working = False

                if not Operator.Asset_is_working:
                    Participant.update_event(3)
                    Operator.Asset.Broken = True
                    Operator.Asset_not_on_RFID = 0
                    # If the boost reminder had been issued right before the asset break
                    GPIO.output(Service.GPIO_out, GPIO.LOW)
                    Operator.Asset.set_next_pimp_reminder(seconds_=8)
                    # Blink all
                    blinker_Queue_Service = Participant.blink_service(Service.ALARM_out, 0.5, queue)
                    blinker_Queue_Operator = Participant.blink_service(Operator.ALARM_out, 0.5, queue)
                    blinker_Queue_Manufacturer = Participant.blink_service(Manufacturer.ALARM_out, 0.5, queue)
                    # END ASSET BREAK

            ##HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##
            if GPIO.input(Operator.Asset.GPIO_to_repair) == 0 and Operator.service_car_at_operators <= 2:
                Operator.service_car_at_operators += 1
            if GPIO.input(Operator.Asset.GPIO_to_repair) == 1:
                Operator.service_car_at_operators = 0

            # check for the status on the repair GPIO of the asset, if a magnet is on the senscor, the GPIO_to_repair of the asset is 0
            if Operator.Asset.Broken and Operator.service_car_at_operators > 1:
                # stop blinking ALL
                Service.repare_Asset(Operator, blinker_Queue_Service, blinker_Queue_Operator,
                                     blinker_Queue_Manufacturer)
                Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=10)
                informed_to_remove_the_service_car = False

            if Operator.service_car_at_operators == 0:
                Service.next_hint_to_return_the_serive_car = 0
                if informed_to_remove_the_service_car:
                    Participant.update_event(12)
                    GPIO.output(Service.GPIO_out, GPIO.LOW)
                    informed_to_remove_the_service_car = False

            if not Service.next_hint_to_return_the_serive_car == 0:
                if not Operator.Asset.Broken and Operator.service_car_at_operators > 1 and datetime.datetime.now() > Service.next_hint_to_return_the_serive_car:
                    # hint: place the service car back to the service station
                    Participant.update_event(11)
                    GPIO.output(Service.GPIO_out, GPIO.HIGH)
                    informed_to_remove_the_service_car = True
                    Service.next_hint_to_return_the_serive_car = datetime.datetime.now() + datetime.timedelta(seconds=20)
            ### END HANDLING THE SERVICE CAR AND REPAIRING THE ASSET##

            ####HANDLING ASSET BOOSTING
            if ASSET_INSTALLED and not Operator.Asset.Broken and Operator.Has_asset:
                if GPIO.input(Operator.Pimp_GPIO) == 0 and Operator.Asset.pimping <= 3:
                    Operator.Asset.pimping += 1
                if GPIO.input(Operator.Pimp_GPIO) == 1 and Operator.Asset.pimping >= -3:
                    Operator.Asset.pimping -= 1

                # remind to pimp the asset
                if not Manufacturer.Bulletin_at_manufacturers_campus and GPIO.input(
                        Operator.Service_Bulletin_GPIO_Measure) == 0 and not Operator.Asset.Pimped:
                    if Operator.Asset.Next_Pimp == 0:
                        # FIRST REMINDER
                        Operator.Asset.set_next_pimp_reminder(seconds_=8)
                    else:
                        if datetime.datetime.now() > Operator.Asset.Next_Pimp:
                            # REMINDER EVENT
                            Participant.update_event(10)
                            GPIO.output(Service.GPIO_out, GPIO.HIGH)
                            Operator.Asset.set_next_pimp_reminder()

                ##BOOSTING THE ASSET
                # if pimping>4 and not Operator.Asset.Pimped and not INFORMED_BULLETIN:
                if Operator.Asset.pimping > 2 and not Operator.Asset.Pimped:
                    Operator.pimp_the_pump()
                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.HIGH)
                    GPIO.output(Manufacturer.GPIO_out, GPIO.HIGH)
                    GPIO.output(Service.GPIO_out, GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output(Operator.Service_Bulletin_GPIO_out, GPIO.LOW)
                    GPIO.output(Manufacturer.GPIO_out, GPIO.LOW)
                    GPIO.output(Service.GPIO_out, GPIO.LOW)

                if Operator.Asset.pimping < 0 and Operator.Asset.Pimped and not Operator.Asset.Broken and Operator.Has_asset:
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

    finally:
        GPIO.cleanup()  # this ensures a clean exit


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
        (ready, msg) = check_ready_to_start()
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


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/start/", StartHandler),
    (r"/stop/", StopHandler),
    (r"/asset_installed/", InstalledHandler),
    # (r"/get_content_xml/", XMLLoader),
], debug=True, **settings)

if __name__ == "__main__":
    try:
        global ASSET_INSTALLED
        ASSET_INSTALLED = False
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
