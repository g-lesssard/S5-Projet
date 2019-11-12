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

picar.setup()

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

speed = 0
forward_speed = 100
backward_speed = 100

back_distance = 10
turn_distance = 20

distance = 100

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
        time.sleep(1)
    fw.turn(45)
    
def car_turn_r():
    print('turn right')
    if last_angle != 90:
        fw.turn_straight()
        time.sleep(1)
    fw.turn(135)

def car_acc():
    global speed
    while speed < forward_speed:
        speed = speed + 10
        bw.forward()
        bw.speed = speed
        print(speed)
        time.sleep(0.1)


def start_avoidance():
    print('start')
    while True:
        car_acc()
#        car_forward()
#        time.sleep(1)
#        car_turn_l()
#        time.sleep(0.2)
#        car_turn_r()
#        time.sleep(0.5)
#        car_backward()
#        time.sleep(1)
        
        
        
        

def stop():
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
        while distance > 10 :
            distance = ua.get_distance()
            print(distance)
            time.sleep(0.2)
            
        start_avoidance()
    except KeyboardInterrupt:
        stop()
