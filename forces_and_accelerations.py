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

#to be determined
MARBLE_RADIUS = 0.0075

#to be determined
FRAME_FRICTION_COEFFICIENT = 0.2

#####################################################
# Forces equations #
#####################################################

# For now, the normal force only consider the gravity to counter. It will need to consider
# other object effect as well as other forces probably.
def marble_normal_force(n):
    normale = n
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
    
    d_force[0] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * velocity[0] ** 2
    d_force[1] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * velocity[1] ** 2
    d_force[2] = -1/2 * drag_coeff_sphere * air_density * cross_section_area * velocity[2] ** 2        
    return d_force

def friction_force(coefficient, direction_v, normale_F):
    direction_v_inv = mu.Vector(direction_v)
    direction_v_inv.negate()
    direction_v_inv.normalize()    
    return direction_v_inv * normale_F.length * coefficient

#####################################################
# Kinematic equations #
#####################################################
def cinematique_position(current_time, init_p = mu.Vector(), init_s = mu.Vector(), init_a = mu.Vector((0.0, 0.0, -GRAVITY))):
    return init_p + init_s * current_time + 0.5 * init_a * current_time ** 2
    
def cinematique_speed(current_time, init_s = mu.Vector(), init_a = mu.Vector((0.0, 0.0, -GRAVITY))):
    return init_s + init_a * current_time

#####################################################
# Collisions #
#####################################################

# Collision section, m in kg and v in m/s
# initial masses are at 2 kg by default so 1/m1 + 1/m2 would be 1 by default
def collision3D(speed1, e = 1.0, normale = mu.Vector((0,0,1)), speed2 = mu.Vector((0,0,0)), m1 = 2.0, m2 = 2.0):
    p = (1 + e) * speed1.dot(normale) * (normale) / (1/m1 + 1/m2)
    return ((speed1 - p), (speed2 + p))

####################################################
# Forces on marble #
####################################################

# marble_pos / _vit / _accel are all in mm, but they NEED to be translate to m through all method
def frame_marble(normale_center_object = None, timestep = 0.1, marble_pos = mu.Vector(), marble_vit = mu.Vector(), marble_accel = mu.Vector()):
    marble_pos = marble_pos / 1000
    marble_vit = marble_vit / 1000
    marble_accel = marble_accel / 1000
    
    normale_edge = normale_center_object.location
    unit_normale = normale_edge - marble_pos
    unit_normale.normalize()
    
    marble_gravity_f = gravity_force(MARBLE_MASS)
    marble_drag_f = drag_force_sphere(MARBLE_RADIUS, marble_vit)
    marble_normale_f = marble_normal_force(unit_normale)
    marble_friction_f = friction_force(FRAME_FRICTION_COEFFICIENT, marble_vit, marble_normale_f)
    
    marble_cumulatif_f = total_force([marble_gravity_f, marble_drag_f, marble_normale_f, marble_friction_f])
    
    marble_accel = marble_cumulatif_f / MARBLE_MASS
    print(str(marble_accel))
