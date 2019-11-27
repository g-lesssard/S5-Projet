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
        self.bw.forward()
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
                self.setWheels(speed=self.speed)
            else:
                self.setWheels(speed=self.speed)
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
                    self.setWheels(speed=self.speed)
                else:
                    self.setWheels(speed=self.speed)
        return self.speed

    def turn(self, angle):
        if angle >=0:
            if self.printing:
                print("turning right at {} degrees".format(angle))
            self.turnRight(angle)
            if angle == 45:
                self.setWheels(wheel='right', speed=0)
            else:
                self.setWheels(wheel='right', speed=self.speed)
            if angle == 40:
                self.setWheels(wheel='right', speed=30)
            else:
                self.setWheels(wheel='right', speed=self.speed)
        elif angle < 0:
            if self.printing:
                print("turning left at {} degrees".format(angle))
            self.turnLeft(abs(angle))
            if angle == -45:
                self.setWheels(wheel='left', speed=0)
            else:
                self.setWheels(wheel='left', speed=self.speed)
            if angle == -40:
                self.setWheels(wheel='left', speed=0)
            else:
                self.setWheels(wheel='left', speed=self.speed)

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

    def setWheels(self, wheel = 'both', speed = 0):
        if wheel is 'left':
            self.bw.right_wheel.speed = abs(speed)
            if speed < 0:
                self.bw.right_wheel.backward()
            else:
                self.bw.right_wheel.forward()
        elif wheel is 'right':
            self.bw.left_wheel.speed = abs(speed)
            if speed < 0:
                self.bw.left_wheel.backward()
            else:
                self.bw.left_wheel.forward()
        elif wheel is 'both':
            self.bw.right_wheel.speed = abs(speed)
            self.bw.left_wheel.speed = abs(speed)
            if speed < 0:
                self.bw.left_wheel.backward()
                self.bw.right_wheel.backward()
            else:
                self.bw.left_wheel.forward()
                self.bw.right_wheel.forward()

        
        


if __name__ == "__main__":

    DC = DirectionControl(printing=True)
    DC.setWheels(speed=100)
    time.sleep(2)
    DC.setWheels(speed=0)

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
    
    
    