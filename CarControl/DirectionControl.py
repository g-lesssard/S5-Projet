from picar import front_wheels
from picar import back_wheels
import time
import picar
import threading


class DirectionControl(object):

    def __init__(self, printing=False):
        self.fw = front_wheels.Front_Wheels(db='confign')
        self.bw = back_wheels.Back_Wheels(db='confign')
        self.printing = printing
        self.speed = 0
        self.moving_thread = None
        self.mutex = threading.Lock()
        self.running = False
        time.sleep(0.3)

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
                if target_speed >= 0:
                    self.speed += step
                    time.sleep(timeout)
                elif target_speed < 0:
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


    def stop(self):
        self.running = False
        self.setSpeed(0, hard_set=True)


if __name__ == "__main__":
    
    #bw = back_wheels.Back_Wheels(db='config')
    #bw.forward()
    #bw.speed = 10
    #time.sleep(1)
    #bw.speed = 0
    #bw.forward()
    #time.sleep(1)

    DC = DirectionControl(printing=True)
    time.sleep(1)
    DC.setSpeed(100)
    time.sleep(1)
    DC.setSpeed(100)
    time.sleep(1)
    DC.setSpeed(0, hard_set=True)
    
    