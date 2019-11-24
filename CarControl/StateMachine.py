from Libraries import line_follower
import Libraries.SunFounder_Line_Follower
import Sensors
from DirectionControl import DirectionControl
import picar
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
        self.line_follower = Sensors.Line_Follower(printing=printing)
        self.dir_control = DirectionControl(printing=printing)

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        self.line_follower.startReading()
        

    def objectDetected(self):
        print("Object in sight, setting avoidance course")
        # call method to modify direction

    def calibrate(self):
        self.line_follower.calibrate()

    def run(self):
        self.dir_control.setSpeed(60)

    def stop(self):
        self.radar.stopReading()
        self.line_follower.stopReading()
        self.dir_control.stop()



########################################################################################################################
