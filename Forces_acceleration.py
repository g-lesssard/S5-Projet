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
def marble_normal_force(sphere_center, marble_center):
    normal_v = mu.Vector((sphere_center[0]-marble_center[0], sphere_center[1]-marble_center[1], sphere_center[2]-marble_center[2]))
    normal_v.normalize()
    z_axis = mu.Vector((0,0,1))
    
    cos_theta = z_axis.dot(normal_v) / (z_axis.length * normal_v.length)
    return normal_v * cos_theta * GRAVITY * MARBLE_MASS

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
    vector_pos_sphere = init_p - sphere_center       
    dist_sphere_pos = vector_pos_sphere.length
    angular_speed = init_s / dist_sphere_pos   
    while iter_nb > 0.0:
        marble_N_F = marble_normal_force(sphere_center, init_p)            
        marble_G_F = gravity_force(MARBLE_MASS)        
        marble_T_F = total_force([marble_N_F, marble_G_F])
        marble_current_accel = marble_T_F / MARBLE_MASS   
        
        vector_pos_sphere = init_p - sphere_center       
        dist_sphere_pos = vector_pos_sphere.length
        angular_accel = marble_current_accel / dist_sphere_pos                
        
        delta_angular_x = cinematique_position(timestep, 0, angular_speed[0], angular_accel[0])
        delta_angular_y = cinematique_position(timestep, 0, angular_speed[1], angular_accel[1])
        delta_angular_z = cinematique_position(timestep, 0, angular_speed[2], angular_accel[2])  
        
        # Verify if need to be negative
        rotQ = ToQuaternion(0.0, delta_angular_x, delta_angular_y)  
        
        print(str(rotQ.to_axis_angle()[0]))
        
        pos_sphereQ = mu.Quaternion(vector_pos_sphere, 0.0)              
        
        pos_sphereQ = mu.Quaternion(QMul(QMul(rotQ, pos_sphereQ), rotQ.inverted()))
        
        # print(str(pos_sphereQ.to_axis_angle()[0]))
        
        new_pos = pos_sphereQ.to_axis_angle()[0] + sphere_center 
        
        angular_speed[0] = cinematique_speed(timestep, angular_speed[0], angular_accel[0])
        angular_speed[1] = cinematique_speed(timestep, angular_speed[1], angular_accel[1])
        angular_speed[2] = cinematique_speed(timestep, angular_speed[2], angular_accel[2])                              
                
        pos_path.append(new_pos) 
        iter_nb -= 1             
        init_p = new_pos 
    return pos_path    