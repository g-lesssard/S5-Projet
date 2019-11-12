from StateMachine import *

########################################################################################################################


class Radar(object):

    def __init__(self):
        self.onObjectDetected = Event()

    def addObserver(self, observer_method):
        self.onObjectDetected += observer_method

    def removeObserver(self, observer_method):
        self.onObjectDetected -= observer_method

    def detectObject(self, distance):
        if distance < 12:
            self.onObjectDetected()


########################################################################################################################
