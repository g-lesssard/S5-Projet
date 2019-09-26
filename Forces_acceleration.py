import bpy
import mathutils as mu
import math
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Custom_MathUtils

import imp
imp.reload(Custom_MathUtils)

# this is optional and allows you to call the functions without specifying the package name
from Custom_MathUtils import *

GRAVITY = 9.807
# Mass in kg
MARBLE_MASS = 4.56/1000

# For now, the normal force only consider the gravity to counter. It will need to consider
# other object effect as well as other forces probably.
def marble_normal_force(normale):
    normale.normalize()
    z_axis = mu.Vector((0,0,1))
    
    cos_theta = z_axis.dot(normale) / (z_axis.length * normale.length)
    return normale * cos_theta * GRAVITY * MARBLE_MASS

def gravity_force(mass):
    return mass * GRAVITY * mu.Vector((0,0,-1))

def total_force(force_list):
    t_force = mu.Vector()
    for force in force_list:
        t_force += force
    return t_force

############ Cinematique
def cinematique_position(current_time, init_p = 0.0, init_s = 0.0, init_a = -9.806):
    return init_p + init_s * current_time + 0.5 * init_a * current_time ** 2
    
def cinematique_speed(current_time, init_s = 0.0, init_a = -9.806):
    return init_s + init_a * current_time

# Collision section, m in kg and v in m/s
# initial masses are at 2 kg by default so 1/m1 + 1/m2 would be 1 by default
def collision3D(speed1, e = 1.0, normale = mu.Vector((0,0,1)), speed2 = mu.Vector((0,0,0)), m1 = 2.0, m2 = 2.0):
    p = (1 + e) * speed1.dot(normale) * (normale) / (1/m1 + 1/m2)
    return ((speed1 - p), (speed2 + p))

# It's important to mention here that timestep aren't binded to keyframes. Logic of correct ratio for 
# keyframes / timestep must be done outside the function.
def marble_path(iter_nb = 1, timestep = 1, init_p = mu.Vector((0,0,0)), init_s = mu.Vector((0,0,0)), sphere_center = mu.Vector((0,0,0))):
    pos_path = [] 
    normale = sphere_center - init_p
    normale.normalize()
    previous_normale = normale
    while iter_nb > 0.0:
        normale = sphere_center - init_p
        normale.normalize()
        marble_N_F = marble_normal_force(normale)            
        marble_G_F = gravity_force(MARBLE_MASS)        
        marble_T_F = total_force([marble_N_F, marble_G_F])
        marble_current_accel = marble_T_F / MARBLE_MASS                   
        
        # To change
        ang = previous_normale.angle(normale)
        axis = previous_normale.cross(normale)
        mat = mu.Matrix.Rotation(ang, 3, axis)
        
        init2 = mat @ previous_normale
        
        print("Prev: " + str(previous_normale))
        print("Final: " + str(normale))
        print("RotM: " + str(mat))
        print("Result Final rotated: " + str(init2) + "\n")
        
        rotated_speed = mat @ init_s
        
        init_p[0] = cinematique_position(timestep, init_p[0], rotated_speed[0], marble_current_accel[0])
        init_p[1] = cinematique_position(timestep, init_p[1], rotated_speed[1], marble_current_accel[1])
        init_p[2] = cinematique_position(timestep, init_p[2], rotated_speed[2], marble_current_accel[2])     
        
        previous_normale = normale                       
                
        init_s[0] = cinematique_speed(timestep, rotated_speed[0], marble_current_accel[0])
        init_s[1] = cinematique_speed(timestep, rotated_speed[1], marble_current_accel[1])
        init_s[2] = cinematique_speed(timestep, rotated_speed[2], marble_current_accel[2])                              
                
        pos_path.append(mu.Vector(init_p)) 
        iter_nb -= 1        
    return pos_path    