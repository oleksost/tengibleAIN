from Participant import Participant

class Service(Participant):

     def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None):
        super(Service, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure, alarm_out)
        self.next_hint_to_return_the_serive_car=0

     def repare_Asset(self, operator, blinker_Queue_Service=None, blinker_Queue_Oerator=None, blinker_Queue_Manufacturer=None):
        operator.Asset.Brocken=False
        Participant.stop_blink_service(blinker_Queue_Service)
        Participant.stop_blink_service(blinker_Queue_Oerator)
        Participant.stop_blink_service(blinker_Queue_Manufacturer)
        Participant.update_event(5)
        #Participant.speak("Service", "Congratulations, you repaired the Asset!")
        operator.Asset_is_working=True
        #update the time for the next random break
        operator.Asset.set_next_break()