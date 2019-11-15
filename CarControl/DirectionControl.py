from picar import front_wheels
from picar import back_wheels
import time
import picar
import threading


class DirectionControl(object):

    def __init__(self):
        self.fw = front_wheels.Front_Wheels(db='config')
        self.bw = back_wheels.Back_Wheels(db='config')
        self.bw.speed = 0
        self.moving_thread = None
        self.mutex = threading.Lock()

    def setSpeed(self,target_speed):
        self.mutex.acquire()
        if target_speed > self.bw.speed:
            while self.bw.speed < target_speed:
                self.bw.speed += 10
                time.sleep(0.1)
        elif target_speed < self.bw.speed:
            while self.bw.speed < target_speed:
                self.bw.speed -= 10
                time.sleep(0.1)
        self.mutex.release()

    def moveCar(self):
        while True:
            if self.bw.speed < 0:
                self.bw.backward()
            elif self.bw.speed > 0:
                self.bw.forward()
    
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

    def start(self):
        self.moving_thread = threading.Thread(target=self.moveCar)
        self.moving_thread.start()

    def kill(self):
        self.moving_thread._stop()

