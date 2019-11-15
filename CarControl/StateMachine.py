from Libraries import line_follower
import Libraries.SunFounder_Line_Follower
import Sensors
import DirectionControl
########################################################################################################################

# States
BASE_LINE_FOLLOWER = 0
WHITE_LINE_FOLLOWER = 1
OBJECT_AVOIDANCE = 2


########################################################################################################################


class Event(object):

    def __init__(self):
        self.eventHandlers = []

    def __iadd__(self, handler):
        self.eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.eventHandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.eventHandlers:
            eventhandler(*args, **keywargs)


########################################################################################################################


class StateController(object):

    def __init__(self, printing=False):
        self.state = BASE_LINE_FOLLOWER
        self.radar = Sensors.Radar(printing=printing)
        self.lf = Sensors.Line_Follower(printing=printing)
        #self.dir_control = DirectionControl.DirectionControl()

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        #self.lf.startReading()
        

    def objectDetected(self):
        print("Object in sight, setting avoidance course")
        # call method to modify direction

    def calibrate(self):
        self.lf.calibrate()

    def run(self):
        pass



########################################################################################################################
