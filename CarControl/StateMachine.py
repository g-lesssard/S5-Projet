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
    LINE_LOSS = auto()
    LINE_CENTERED = auto()
    AVOID_OBSTACLE = auto()
    PIETONS = auto()
    LOOP = auto()
    DO_STOP = auto()
    TEST = auto()
    SHARP_TURN = auto()
    SLALOM = auto()
    EXITING_SLALOM = auto()
    ENTERING_SLALOM = auto()


########################################################################################################################


class Event(object):

    def __init__(self):
        self.eventHandlers = []

    def __iadd__(self, handler):
        self.eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        if handler in self.eventHandlers:
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
        self.line_follower = Sensors.Line_Follower(printing=False)
        self.dir_control = DirectionControl(printing=False)
        self.angle = 0
        self.obstacle_count = 0
        self.cruising_speed = 0

        self.recovering_angle = 0

    def startReadingThreads(self):
        self.radar.startReading()
        self.radar.addObserver(self.objectDetected)
        self.line_follower.startReading()
        self.line_follower.addObserver(observer_method=self.pietonsDetected, event='pietons')
        self.line_follower.addObserver(observer_method=self.sharpTurnDetected, event='sharp_turn')
        

    def objectDetected(self):
        
        if self.state is State.SLALOM:
            self.line_follower.removeObserver(event='line_lost', observer_method=self.lineLost)
            self.line_follower.removeObserver(event='line_centered', observer_method=self.lineCentered())
        if self.state is State.BASE_LINE_FOLLOWER or self.state is State.SLALOM:
            print("Obstacle detected, setting avoidance course...")
            self.state = State.AVOID_OBSTACLE
    
    def pietonsDetected(self):
        if self.state is State.BASE_LINE_FOLLOWER:
            print("Pietons detected, stopping...")
            self.state = State.PIETONS

    def lineLost(self):
        if self.state is State.SLALOM:
            print("Line lost, activating criss cross")
            self.state = State.LINE_LOSS
            self.recovering_angle = -0.7*self.angle

    def lineCentered(self):
        if self.state is State.LINE_LOSS:
            print("Line centered, going back to line following")
            self.state = State.SLALOM
        if self.state is State.SHARP_TURN:
            print("Entering Slalom...")
            self.state = State.ENTERING_SLALOM

    def lineFound(self):
        if self.state is State.LINE_FINDER:
            print("Line found, following it...")
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
        print('Car state is: {}'.format(self.state))
        if self.state is State.TEST:
            self.dir_control.setSpeed(20)
        elif self.state is State.START:
            self.start()
        elif self.state is State.BASE_LINE_FOLLOWER:
            self.follow_line()
        elif self.state is State.AVOID_OBSTACLE:
            if self.obstacle_count == 0:
                self.avoidObstacleRight()
            elif self.obstacle_count == 1:
                self.avoidObstacleLeft()
        elif self.state is State.LINE_FINDER:
            time.sleep(0.1)
        elif self.state is State.PIETONS:
            self.savePietons()
        elif self.state == State.DO_STOP:
            self.finish()
        elif self.state is State.SHARP_TURN:
            self.sharpTurn()
        elif self.state is State.SLALOM:
            self.follow_line_slalom()
        elif self.state is State.LINE_LOSS:
            self.recovering_line()
        elif self.state is State.ENTERING_SLALOM:
            self.enterSlalom()

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
            self.angle = 44
        elif refs == [0,0,0,1,1]:
            self.angle = 40
        elif refs == [0,0,0,1,0]:
            self.angle = 20
        elif refs == [0,0,1,1,0]:
            self.angle = 8
        elif refs == [1,0,0,0,0]:
            self.angle = -44
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
        self.dir_control.setSpeed(self.cruising_speed)
        refs = self.line_follower.getData()
        if refs == [0,0,1,0,0]:
            self.angle = -0
        elif refs == [0,0,0,0,1]:
            self.angle = 45
        elif refs == [0,0,0,1,1]:
            self.angle = 45
        elif refs == [0,0,0,1,0]:
            self.angle = 36
        elif refs == [0,0,1,1,0]:
            self.angle = 26
        elif refs == [1,0,0,0,0]:
            self.angle = -45
        elif refs == [1,1,0,0,0]:
            self.angle = -45
        elif refs == [0,1,0,0,0]:
            self.angle = -36
        elif refs == [0,1,1,0,0]:
            self.angle = -26
        else:
            pass
        self.dir_control.turn(self.angle)

    def recovering_line(self):
        self.dir_control.speed = 0
        self.angle = self.recovering_angle
        self.dir_control.turn(self.angle)
        self.dir_control.speed = -50


    def avoidObstacleRight(self):
        self.radar.removeObserver(observer_method=self.objectDetected)
        self.angle = 40
        self.dir_control.turn(self.angle)
        time.sleep(1.5)
        
        self.angle = 0
        self.dir_control.turn(self.angle)
        time.sleep(1.7)
        
        self.angle = -44
        self.dir_control.turn(self.angle)
        time.sleep(0.5)

        self.angle = -40
        self.dir_control.turn(self.angle)
        time.sleep(2)
        
        self.angle = -44
        self.dir_control.turn(self.angle)
        time.sleep(2.5)

        self.angle = -25
        self.dir_control.turn(self.angle)
        
        print("Obstacle avoided, going back to line following")
        self.obstacle_count += 1
        self.line_follower.addObserver(observer_method=self.lineFound, event='line_found')
        self.state = State.LINE_FINDER

    def sharpTurn(self):
        self.line_follower.removeObserver(observer_method=self.sharpTurnDetected, event='sharp_turn')
        self.radar.addObserver(observer_method=self.objectDetected)
        self.dir_control.turnRight(40)
        time.sleep(1)
        self.dir_control.speed = 0
        time.sleep(0.3)
        self.dir_control.turnLeft(30)
        self.cruising_speed = -50
        self.dir_control.speed = self.cruising_speed
        time.sleep(3)


        self.cruising_speed = 60
        self.dir_control.speed = self.cruising_speed
        self.dir_control.turnRight(30)
        time.sleep(3)
        self.dir_control.turn(0)
        self.line_follower.addObserver(event='line_lost', observer_method=self.lineLost)
        self.line_follower.addObserver(event='line_centered', observer_method=self.lineCentered)
        self.state = State.SLALOM

    def sharpTurn2(self):
        self.line_follower.removeObserver(observer_method=self.sharpTurnDetected, event='sharp_turn')
        self.radar.addObserver(observer_method=self.objectDetected)
        self.dir_control.turnRight(40)
        time.sleep(0.1)
        self.dir_control.speed = 0
        self.dir_control.turnLeft(30)
        self.cruising_speed = -20
        self.dir_control.speed = self.cruising_speed
        self.line_follower.addObserver(event='line_lost', observer_method=self.lineLost)
        self.line_follower.addObserver(event='line_centered', observer_method=self.lineCentered)


    def enterSlalom(self):
        self.angle = 40
        self.dir_control.turnRight(self.angle)
        self.cruising_speed = 60
        self.dir_control.speed = self.cruising_speed
        self.state = State.SLALOM


    def avoidObstacleLeft(self):
        self.radar.removeObserver(self.objectDetected)
        self.angle = -30
        self.dir_control.turn(self.angle)
        time.sleep(1.5)
        self.angle = 0
        self.dir_control.turnRight(self.angle)
        time.sleep(1)
        self.angle = 30
        self.dir_control.turn(self.angle)
        self.cruising_speed = 60
        self.dir_control.speed = self.cruising_speed
        self.state = State.BASE_LINE_FOLLOWER


    def savePietons(self):
        self.dir_control.speed = 40
        time.sleep(2.69)
        self.dir_control.speed = 0
        time.sleep(2)
        self.cruising_speed = 60
        self.dir_control.speed = self.cruising_speed
        self.state = State.BASE_LINE_FOLLOWER

    def finish(self):
        self.dir_control.turn(0)
        self.dir_control.speed = 0



        
########################################################################################################################

if __name__ == '__main__':
    master = StateController(printing=True)

    master.run()
    master.stop()