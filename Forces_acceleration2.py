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

def drag_force_sphere(radius, velocity = mu.Vector()):
    air_density = 1.225
    drag_coeff_sphere = 0.47
    cross_section_area = math.pi * (radius ** 2)
    d_force = mu.Vector()
    
    d_force[0] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * (velocity[0] ** 2)
    d_force[1] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * (velocity[1] ** 2)
    d_force[2] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * (velocity[2] ** 2)
    return d_force

def friction_force(coefficient, direction_v, normale_F):
    direction_v_inv = mu.Vector(direction_v)
    direction_v_inv.negate()
    direction_v_inv.normalize()
    # /10 comes from scaling done in blender. 3 cm in real life = 30 cm in blender for example
    return direction_v_inv * normale_F.length * coefficient / 10

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
def marble_path(iter_nb = 1, timestep = 1, init_p = mu.Vector((0,0,0)), init_s = mu.Vector((0,0,0)), sphere_center = mu.Vector((0,0,0)), init_rot = mu.Vector()):
    pos_path = [] 
    rot_path = []     
    normale = sphere_center - init_p
    init_radius = normale.length
    normale.normalize()
    previous_normale = normale   
    rot_axis = mu.Vector() 
    while iter_nb > 0.0:
        if math.sqrt(init_p[0]**2 + init_p[1]**2) <= 17.7:
            normale = sphere_center - init_p
        elif (abs(init_p[0]) <= 27.5 and abs(init_p[1]) <= 27.5) or init_p[2] <= -22.5:
            normale = mu.Vector((0.0, 0.0, 1.0))
            previous_normale = normale            
        else:
            normale = mu.Vector()
        normale_normalized = normale
        normale_normalized.normalize()
        
        # Rotate speed
        ang = previous_normale.angle(normale_normalized) if normale_normalized.length > 0.0 else mu.Vector()
        axis = previous_normale.cross(normale_normalized) if normale_normalized.length > 0.0 else mu.Vector()
        mat = mu.Matrix.Rotation(ang, 3, axis) if normale_normalized.length > 0.0 else mu.Matrix()
             
        rotated_speed = mat @ init_s if normale_normalized.length > 0.0 else init_s
        
        marble_N_F = marble_normal_force(normale_normalized) if normale_normalized.length > 0.0 else mu.Vector()            
        marble_G_F = gravity_force(MARBLE_MASS)       
        marble_D_F = drag_force_sphere(7.5, init_s) if normale_normalized.length > 0.0 else mu.Vector()    
        marble_F_F = friction_force(0.2, rotated_speed, marble_N_F) if normale_normalized.length > 0.0 else mu.Vector()
        marble_T_F = total_force([marble_N_F, marble_G_F, marble_D_F, marble_F_F])
        marble_current_accel = marble_T_F / MARBLE_MASS  
        print(marble_current_accel)                                 
        
        init_p[0] = cinematique_position(timestep, init_p[0], rotated_speed[0], marble_current_accel[0])
        init_p[1] = cinematique_position(timestep, init_p[1], rotated_speed[1], marble_current_accel[1])
        init_p[2] = cinematique_position(timestep, init_p[2], rotated_speed[2], marble_current_accel[2])  
        
        # Rotation
        rot_axis = normale_normalized.cross(rotated_speed) if normale_normalized.length > 0.0 else rot_axis
        rot_axis.normalize()
        rotation = rotated_speed.length * 1.5 * timestep * 2 * math.pi               
        
        rotQ = mu.Quaternion(rot_axis, rotation)
        init_rotQ = init_rot.to_quaternion()
        new_rotQ = rotQ @ init_rotQ
        init_rot = (new_rotQ).to_euler()         
        rot_path.append(new_rotQ)
        
        # Correct the new position to fit the good radius from sphere center to marble
        if (math.sqrt(init_p[0]**2 + init_p[1]**2) <= 0.177):
            temp_normale = sphere_center - init_p
            init_p = sphere_center - ((init_radius / temp_normale.length) * temp_normale)
        elif (abs(init_p[0]) <= 0.275 and abs(init_p[1]) <= 0.275) or init_p[2] <= -0.225:
            if init_p[2] <= -0.225:
                init_p[2] = -0.225
            rotated_speed[2] = 0.0
        
        previous_normale = normale_normalized                       
                
        init_s[0] = cinematique_speed(timestep, rotated_speed[0], marble_current_accel[0])
        init_s[1] = cinematique_speed(timestep, rotated_speed[1], marble_current_accel[1])
        init_s[2] = cinematique_speed(timestep, rotated_speed[2], marble_current_accel[2])                        
                
        pos_path.append(mu.Vector(init_p))
        iter_nb -= 1        
    return pos_path, rot_path    