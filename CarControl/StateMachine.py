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
    START = auto()
    BASE_LINE_FOLLOWER = auto()
    LINE_FINDER = auto()
    AVOID_OBSTACLE = auto()
    PIETONS = auto()
    LOOP = auto()
    DO_STOP = auto()
    TEST = auto()
    SHARP_TURN = auto()
    SLALOM = auto()


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
        self.state = State.START
        self.radar = Sensors.Radar(printing=False)
        self.line_follower = Sensors.Line_Follower(printing=True)
        self.dir_control = DirectionControl(printing=False)
        self.angle = 0
        self.obstacle_count = 0
        self.cruising_speed = 0

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        self.line_follower.startReading()
        self.line_follower.addObserver(observer_method=self.pietonsDetected, event='pietons')
        self.line_follower.addObserver(observer_method=self.sharpTurnDetected, event='sharp_turn')
        

    def objectDetected(self):
        print("Obstacle detected, setting avoidance course...")
        self.state = State.AVOID_OBSTACLE
    
    def pietonsDetected(self):
        print("Pietons detected, stopping...")
        self.state = State.PIETONS

    def lineFound(self):
        print("Line found, following it...")
        #self.line_follower.removeObserver(observer_method=self.lineFound, event='line_found')
        self.state = State.BASE_LINE_FOLLOWER

    def sharpTurnDetected(self):
        print('Sharp turn detected')
        self.state = State.SHARP_TURN

    def calibrate(self):
        self.dir_control.setTurningOffset()
        self.line_follower.calibrate()
        self.dir_control.turn(0)
        input("Press ENTER to start...")

    def run(self):
        #print('Car state is: {}'.format(self.state))
        if self.state is State.TEST:
            self.dir_control.setSpeed(20)
        if self.state is State.START:
            self.start()
        if self.state is State.BASE_LINE_FOLLOWER:
            self.follow_line()
        if self.state is State.AVOID_OBSTACLE:
            if self.obstacle_count == 0:
                self.avoidObstacleRight()
            elif self.obstacle_count == 1:
                self.avoidObstacleLeft()
        if self.state is State.LINE_FINDER:
            time.sleep(0.1)
        if self.state is State.PIETONS:
            self.savePietons()
        if self.state == State.DO_STOP:
            self.finish()
        if self.state is State.SHARP_TURN:
            self.sharpTurn()
        if self.state is State.SLALOM:
            self.follow_line_slalom()

    def start(self):
        self.cruising_speed = 60
        self.dir_control.setSpeed(self.cruising_speed)
        self.state = State.BASE_LINE_FOLLOWER

    def stop(self):
        self.radar.stopReading()
        self.line_follower.stopReading()
        self.dir_control.stop()

    def follow_line(self):
        refs = self.line_follower.getData()
        if refs == [0,0,1,0,0]:
            self.angle = -0
        elif refs == [0,0,0,0,1]:
            self.angle = 45
        elif refs == [0,0,0,1,1]:
            self.angle = 40
        elif refs == [0,0,0,1,0]:
            self.angle = 20
        elif refs == [0,0,1,1,0]:
            self.angle = 8
        elif refs == [1,0,0,0,0]:
            self.angle = -45
        elif refs == [1,1,0,0,0]:
            self.angle = -40
        elif refs == [0,1,0,0,0]:
            self.angle = -20
        elif refs == [0,1,1,0,0]:
            self.angle = -8
        else:
            pass
        self.dir_control.turn(self.angle)

    def follow_line_slalom(self):
        refs = self.line_follower.getData()
        if refs == [0,0,1,0,0]:
            self.angle = -0
        elif refs == [0,0,0,0,1]:
            self.angle = 45
        elif refs == [0,0,0,1,1]:
            self.angle = 41
        elif refs == [0,0,0,1,0]:
            self.angle = 31
        elif refs == [0,0,1,1,0]:
            self.angle = 21
        elif refs == [1,0,0,0,0]:
            self.angle = -45
        elif refs == [1,1,0,0,0]:
            self.angle = -41
        elif refs == [0,1,0,0,0]:
            self.angle = -31
        elif refs == [0,1,1,0,0]:
            self.angle = -21
        else:
            pass
        self.dir_control.turn(self.angle)
        

    def avoidObstacleRight(self):
        self.angle = 30
        self.dir_control.turn(self.angle)
        time.sleep(1.5)
        
        self.angle = 0
        self.dir_control.turn(self.angle)
        time.sleep(1)
        
        self.angle = -45
        self.dir_control.turn(self.angle)
        time.sleep(0.5)

        self.angle = -40
        self.dir_control.turn(self.angle)
        time.sleep(2)
        
        self.angle = -45
        self.dir_control.turn(self.angle)
        time.sleep(2)
        
        print("Obstacle avoided, going back to line following")
        self.obstacle_count += 1
        self.line_follower.addObserver(observer_method=self.lineFound, event='line_found')
        self.state = State.LINE_FINDER

    def sharpTurn(self):
        self.dir_control.setSpeed(0)
        self.dir_control.turnLeft(44)
        self.cruising_speed = -50
        self.dir_control.setSpeed(self.cruising_speed)
        time.sleep(1.5)

        self.dir_control.turnRight(0)
        self.cruising_speed = 45
        self.dir_control.setSpeed(self.cruising_speed)
        time.sleep(0.3)

        self.dir_control.turnRight(30)
        time.sleep(0.4)
        self.state = State.SLALOM      

    def avoidObstacleLeft(self):
        self.angle = -30
        self.dir_control.turn(-30)
        time.sleep(1.5)
        self.angle = 0
        self.dir_control.turnRight(self.angle)
        time.sleep(2)
        self.angle = 30
        self.dir_control.turn(30)
        self.radar.removeObserver(self.objectDetected)
        self.cruising_speed = 60
        self.dir_control.setSpeed(self.cruising_speed)
        self.state = State.BASE_LINE_FOLLOWER


    def savePietons(self):
        self.line_follower.removeObserver(observer_method=self.sharpTurnDetected, event='sharp_turn')
        self.dir_control.setSpeed(30)
        time.sleep(2.69)
        self.dir_control.setSpeed(0)
        time.sleep(2)
        self.state = State.BASE_LINE_FOLLOWER

    def finish(self):
        self.dir_control.turn(0)
        self.dir_control.setSpeed(0)



        
########################################################################################################################

if __name__ == '__main__':
    master = StateController(printing=True)

    master.state = State.BASE_LINE_FOLLOWER
    master.run()
    master.stop()