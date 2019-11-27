from Libraries import line_follower
import Libraries.SunFounder_Line_Follower
import Sensors
from DirectionControl import DirectionControl
import picar
from enum import Enum, auto
import time
########################################################################################################################

# States
class State(Enum):
    BASE_LINE_FOLLOWER = auto()
    AVOID_OBSTACLE = auto()
    PIETONS = auto()
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
        self.angle = 0

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        self.line_follower.startReading()
        self.line_follower.addObserver(self.pietonsDetected)
        

    def objectDetected(self):
        print("Obstacle detected, setting avoidance course...")
        self.state = State.AVOID_OBSTACLE
    
    def pietonsDetected(self):
        print("Pietons detected, stopping...")
        self.state = State.PIETONS

        

    def calibrate(self):
        self.dir_control.setTurningOffset()
        self.line_follower.calibrate()
        self.dir_control.turn(0)
        input("Press ENTER to start...")

    def run(self):
        if self.state is State.TEST:
            self.dir_control.setSpeed(20)
        if self.state is State.BASE_LINE_FOLLOWER:
            self.follow_line()
        if self.state is State.AVOID_OBSTACLE:
            self.avoidObstacle()
        if self.state is State.PIETONS:
            self.savePietons()


    def stop(self):
        self.radar.stopReading()
        self.line_follower.stopReading()
        self.dir_control.stop()

    def follow_line(self):
        self.dir_control.setSpeed(60)
        refs = self.line_follower.getData()
        print(refs)
        if refs == [0,0,1,0,0]:
            self.angle = -0
        elif refs == [0,0,0,0,1]:
            self.angle = 45
        elif refs == [0,0,0,1,1]:
            self.angle = 35
        elif refs == [0,0,0,1,0]:
            self.angle = 20
        elif refs == [0,0,1,1,0]:
            self.angle = 10
        elif refs == [1,0,0,0,0]:
            self.angle = -45
        elif refs == [1,1,0,0,0]:
            self.angle = -35
        elif refs == [0,1,0,0,0]:
            self.angle = -20
        elif refs == [0,1,1,0,0]:
            self.angle = -10
        else:
            pass
        self.dir_control.turn(self.angle)

    def avoidObstacle(self):
        time.sleep(0.1)
        self.dir_control.setSpeed(0)
        time.sleep(2)
        print("Obstacle avoided, going back to line following")
        self.state = State.BASE_LINE_FOLLOWER

    def savePietons(self):
        self.dir_control.setSpeed(30)
        time.sleep(2)
        self.dir_control.setSpeed(0)
        time.sleep(1)
        self.state = State.BASE_LINE_FOLLOWER



        
########################################################################################################################

if __name__ == '__main__':
    master = StateController(printing=True)

    master.state = State.BASE_LINE_FOLLOWER
    master.run()
    master.stop()