#!/usr/bin/env python
'''
**********************************************************************
* Filename    : ultra_sonic_avoidance.py
* Description : An example for sensor car kit to followe light
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-27    New release
**********************************************************************
'''

from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import random

picar.setup()

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

forward_speed = 50
backward_speed = 50

back_distance = 10
turn_distance = 20

last_angle = 90

def car_forward():
    print('forward')
    bw.forward()
    bw.speed = forward_speed
        
def car_backward():
    print('backward')
    bw.backward()
    bw.speed = backward_speed

def car_turn_l():
    print('turn left')
    if last_angle != 90:
        fw.turn_straight()
    fw.turn(45)
    last_angle = 45
    
def car_turn_r():
    print('turn right')
    if last_angle != 90:
        fw.turn_straight()
    fw.turn(135)
    last_angle = 135


def start_avoidance():
    print('start')
    while True:
        distance = ua.get_distance()
        print("distance: %scm" % distance)
        if distance <= back_distance:
            fw.turn_straight()
            car_backward()
        elif distance <= turn_distance:
            if random.randint(0, 1) == 1:
                car_turn_l()
            else:
                car_turn_r()
            car_forward()
        else:
            fw.turn_straight()
            car_forward()
        time.sleep(0.5)
        
def stop():
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
        start_avoidance()
    except KeyboardInterrupt:
        stop()

