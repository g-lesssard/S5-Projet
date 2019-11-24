from picar import front_wheels
from picar import back_wheels
from picar import filedb
import time
import picar
import threading

config_file = '/home/projet/CarControl/config'

class DirectionControl(object):

    def __init__(self, printing=False):
        self.fw = front_wheels.Front_Wheels(db=config_file)
        self.bw = back_wheels.Back_Wheels(db=config_file)
        self.printing = printing
        self.speed = 0
        self.moving_thread = None
        self.mutex = threading.Lock()
        self.running = False
        time.sleep(0.3)

    def setTurningOffset(self):
        self.turn(0)
        db = filedb.fileDB(db=config_file)
        offset = int(db.get('turning_offset'))
        print('Current offset is: {}'.format(offset))
        new_offset = int(input("Enter new offset to set new offset or same offset to exit: "))
        if new_offset == offset:
            return
        else:
            db.set('turning_offset', new_offset)
            self.fw= front_wheels.Front_Wheels(db=config_file)
            self.setTurningOffset()

    def setSpeed(self, target_speed, hard_set=False):
        target_speed = int(target_speed)
        step = 1
        timeout = 0.01
        if hard_set:
            self.speed = target_speed
            if self.printing:
                print(self.speed)
            if self.speed >= 0:
                self.bw.forward()
                self.bw.speed = abs(self.speed)
            else:
                self.bw.backward()
                self.bw.speed = abs(self.speed)
            return self.speed
        else:
            while self.speed != target_speed:
                if target_speed >= self.speed:
                    self.speed += step
                    time.sleep(timeout)
                elif target_speed < self.speed:
                    self.speed -= step
                    time.sleep(timeout)

                if self.printing:
                    print(self.speed)

                if self.speed >= 0:
                    self.bw.backward()
                    self.bw.speed = abs(self.speed)
                else:
                    self.bw.forward()
                    self.bw.speed = abs(self.speed)
        return self.speed

    def turn(self, angle):
        if angle >=0:
            if print:
                print("turning right at {} degrees".format(angle))
            self.turnRight(angle)
        elif angle < 0:
            if print:
                print("turning left at {} degrees".format(angle))
            self.turnLeft(abs(angle))

    def turnRight(self,angle): 
        if angle > 45: 
            print("Cannot turn at such a big angle...") 
        else: 
            self.fw.turn(90 + angle) 
 
    def turnLeft(self,angle): 
        if angle > 45: 
            print("Cannot turn at such a big angle...") 
        else: 
            self.fw.turn(90 - angle) 


    def stop(self):
        self.running = False
        self.setSpeed(0, hard_set=True)


if __name__ == "__main__":
    

    DC = DirectionControl(printing=True)
    time.sleep(1)
    DC.setSpeed(100)
    time.sleep(1)
    DC.setSpeed(-100)
    time.sleep(1)
    DC.setSpeed(0)

    angles = [10, 20, 25, 30, 45]
    DC.turnLeft(0)
    DC.setTurningOffset()
    for angle in angles:
        DC.turnRight(angle)
        time.sleep(0.5)
        DC.turnLeft(0)
        time.sleep(0.5)
        DC.turnLeft(angle)
        time.sleep(0.5)
        DC.turnLeft(0)
    
    
    