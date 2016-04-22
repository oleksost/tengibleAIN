from Participant import Participant

class Service(Participant):

     def __init__(self, gpio_out, service_bulletin_out=None, service_bullete_measure=None, alarm_out=None):
        super(Service, self).__init__(gpio_out, service_bulletin_out, service_bullete_measure, alarm_out)
        self.next_hint_to_return_the_serive_car=0

     def repare_Asset(self, operator, service, manufacturer):
         if not operator.Asset is None:
           operator.Asset.Broken=False
           operator.Asset.set_next_break()
           operator.Asset_is_working=True
         Participant.stop_blinking(service.Blinker_queue)
         Participant.stop_blinking(operator.Blinker_queue)
         Participant.stop_blinking(manufacturer.Blinker_queue)
         #Participant.update_event(5)
         #Participant.speak("Service", "Congratulations, you repaired the Asset!")
         #update the time for the next break
         Participant.update_event(5)
