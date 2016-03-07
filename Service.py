from Participant import Participant

class Service(Participant):
     def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None):
        super(Service, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure)
    
     def repare_Asset(self, operator, blinker_Queue):
        operator.Asset.Brocken=False
        self.stop_blink_service(blinker_Queue)
        Participant.speak("Service", "Congratulations, you repaired the Asset!")
        operator.Asset_is_working=True
        #update the time for the next random break
        operator.Asset.set_next_break()    