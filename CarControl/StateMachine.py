from Libraries import line_follower
import Libraries.SunFounder_Line_Follower
import Sensors
from DirectionControl import DirectionControl
import picar
from enum import Enum, auto
########################################################################################################################

# States
class State(Enum):
    BASE_LINE_FOLLOWER = auto()
    AVOID_OBSTACLE = auto()
    LOOP = auto()
    DO_STOP = auto()
    TEST = auto()


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
        self.state = State.BASE_LINE_FOLLOWER
        self.radar = Sensors.Radar(printing=False)
        self.line_follower = Sensors.Line_Follower(printing=False)
        self.dir_control = DirectionControl(printing=printing)

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        self.line_follower.startReading()
        

    def objectDetected(self):
        #self.state = State.AVOID_OBSTACLE
        pass
        

    def calibrate(self):
        self.dir_control.setTurningOffset()
        self.line_follower.calibrate()
        self.dir_control.turn(0)
        input("Press ENTER to start...")

    def run(self):
        if self.state is State.TEST:
            print('Test state not implemented')
        if self.state is State.BASE_LINE_FOLLOWER:
            print('Following line')
            self.follow_line()
        if self.state == State.AVOID_OBSTACLE:
            pass

    def stop(self):
        self.radar.stopReading()
        self.line_follower.stopReading()
        self.dir_control.stop()

    def follow_line(self):
        self.dir_control.setSpeed(60)
        angle = 0
        refs = self.line_follower.getData()
        print(refs)
        if refs == [0,0,1,0,0]:
            angle = -0
        elif refs == [0,0,0,0,1]:
            angle = 45
        elif refs == [0,0,0,1,1]:
            angle = 35
        elif refs == [0,0,0,1,0]:
            angle = 25
        elif refs == [0,0,1,1,0]:
            angle = 15
        elif refs == [1,0,0,0,0]:
            angle = -45
        elif refs == [1,1,0,0,0]:
            angle = -35
        elif refs == [0,1,0,0,0]:
            angle = -25
        elif refs == [0,1,1,0,0]:
            angle = -15
        else:
            angle = 45
        self.dir_control.turn(angle)
        
########################################################################################################################

if __name__ == '__main__':
    master = StateController(printing=True)

    master.state = State.BASE_LINE_FOLLOWER
    master.run()
    master.stop()