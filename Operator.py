from Participant import Participant

class Operator(Participant):
     def __init__(self, gpio_out, service_bulleten_out=None, service_bullete_measure=None, has_asset=False, asset=None, asset_works=False, on_RFID=0, imformed_about_recent_update=False):
        super(Operator, self).__init__(gpio_out, service_bulleten_out, service_bullete_measure, has_asset, asset, asset_works, on_RFID=0)
        self.Imformed_about_recent_update=imformed_about_recent_update
        