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
FRAME_FRICTION_COEFFICIENT = 0.015

# Substract volume radius
# would be 140mm - 7.5mm, but as sphere resolution is not good, this is the real radius in blender
FRAME_RADIUS = 0.13241060829162598

#####################################################
# Forces equations #
#####################################################

# For now, the normal force only consider the gravity to counter. It will need to consider
# other object effect as well as other forces probably.
def marble_normal_force(n, gravity_f):
    normale = n
    normale.normalize()
    z_axis = mu.Vector((0,0,1))
    
    # / (z_axis.length * normale.length) is not used as they both are unit vectors
    cos_theta = z_axis.dot(normale) 
    return normale * cos_theta * gravity_f.length

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
    print("Friction force calculation.......")
    print("Initial friction speed: " + str(direction_v))
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
    p = (1 + e) * speed1.dot(normale) * (normale) / (1.0/m1 + 1.0/m2)
    return ((speed1 - p), (speed2 + p))

####################################################
# Forces on marble #
####################################################

def forces_accel_on_marble(marble_vit = mu.Vector(), unit_normale = mu.Vector((0.0, 0.0, 1.0)), is_marble_in_contact = False):
    marble_forces_list = []   
    marble_gravity_f = gravity_force(MARBLE_MASS)
    marble_forces_list.append(marble_gravity_f)
    marble_forces_list.append(drag_force_sphere(MARBLE_RADIUS, marble_vit))
    if is_marble_in_contact:
        marble_normale_f = marble_normal_force(unit_normale, marble_gravity_f)
        marble_forces_list.append(marble_normale_f)
        marble_forces_list.append(friction_force(FRAME_FRICTION_COEFFICIENT, marble_vit, marble_normale_f))
        
    marble_cumulatif_f = total_force(marble_forces_list)
    
    return marble_cumulatif_f / MARBLE_MASS

###################################################
# Utility functions #
###################################################

# Correction of position in case marble is IN frame
def correct_marble_pos(marble_pos, normale_edge):
    temp_normale = normale_edge - marble_pos    
    return normale_edge - ((FRAME_RADIUS / temp_normale.length) * temp_normale)

def update_new_pos(timestep, marble_pos, marble_vit, marble_accel, normale_edge, is_marble_in_contact = False):
    new_pos = mu.Vector()
    new_pos[0] = cinematique_position(timestep, marble_pos[0], marble_vit[0], marble_accel[0])
    new_pos[1] = cinematique_position(timestep, marble_pos[1], marble_vit[1], marble_accel[1])
    new_pos[2] = cinematique_position(timestep, marble_pos[2], marble_vit[2], marble_accel[2])
    if is_marble_in_contact:
        new_pos = correct_marble_pos(new_pos, normale_edge)
    return new_pos
    
def update_new_vit(timestep, speed, accel):   
    new_speed = mu.Vector() 
    new_speed[0] = cinematique_speed(timestep, speed[0], accel[0])
    new_speed[1] = cinematique_speed(timestep, speed[1], accel[1])
    new_speed[2] = cinematique_speed(timestep, speed[2], accel[2])  
    return new_speed

def get_unit_normale(final_point, init_point):
    unit_normale = final_point - init_point
    unit_normale.normalize()
    return unit_normale

# Get speed directly on frame plane
def get_rotated_speed(unit_normale, prev_unit_normale, vit_to_rotate):        
    ang = prev_unit_normale.angle(unit_normale) if unit_normale.length > 0.0 else mu.Vector()
    axis = prev_unit_normale.cross(unit_normale) if unit_normale.length > 0.0 else mu.Vector()
    mat = mu.Matrix.Rotation(ang, 3, axis) if unit_normale.length > 0.0 else mu.Matrix()
             
    return mat @ vit_to_rotate if unit_normale.length > 0.0 else vit_to_rotate

# Return estimation of the carframe's speed from frame (m/s)
def get_frame_speed(current_frame, timestep):
    if current_frame < 1:
        return mu.Vector()
    
    car_frame = bpy.data.objects["CarFrame"]
    bpy.context.scene.frame_set(current_frame - 1)
    init_p = mu.Vector(car_frame.location)
    bpy.context.scene.frame_set(current_frame)
    final_p = mu.Vector(car_frame.location)
    return (final_p - init_p) / (1000.0 * timestep)

# Verify if should be pos-2 to pos0 or pos-1 to pos+1
# Don't know the behavior when at the end of animation
# Can be greatly optimize in order to not compute velocity each time at each iteration
# Return current position, velocity, acceleration of carframe
def get_frame_pos_vit_accel(current_frame, timestep):
    car_frame = bpy.data.objects["CarFrame"]
    
    init_v = mu.Vector()    
    final_v = mu.Vector()
        
    bpy.context.scene.frame_set(current_frame - 1)
    prev_pos = car_frame.matrix_world @ mu.Vector((0.0, 0.0, 0.0)) / 1000.0
    
    bpy.context.scene.frame_set(current_frame)
    current_pos = car_frame.matrix_world @ mu.Vector((0.0, 0.0, 0.0)) / 1000.0
    
    bpy.context.scene.frame_set(current_frame + 1)
    future_pos = car_frame.matrix_world @ mu.Vector((0.0, 0.0, 0.0)) / 1000.0
    
    current_vit = (current_pos - prev_pos) / timestep
    future_vit = (future_pos - current_pos) / timestep
    
    current_accel = (future_vit - current_vit) / timestep
    
    return current_pos, current_vit, current_accel

# marble_pos / _vit / _accel are all in mm, but they NEED to be translate to m through all method
def frame_marble(normale_center_object = None, timestep = 1/60, pos = mu.Vector(), marble_vit = mu.Vector(), prev_normale = mu.Vector((0.0, 0.0, 1.0)), current_frame = 0):
    # Find frame current speed from previous frames
    frame_pos, frame_vit, frame_accel = get_frame_pos_vit_accel(current_frame, timestep)   
#    print("Frame current position: " + str(frame_pos * 1000.0) + "(mm)")  
#    print("Frame current velocity: " + str(frame_vit * 1000.0) + "(mm/s)")  
#    print("Frame current acceleration: " + str(frame_accel * 1000.0) + "(mm/s2)")  
#    print()
    
    # Convert to m from mm (vit and pos are not necessary, but are like that for lisibility
    marble_pos = pos / 1000.0 
    
    normale_edge = mu.Vector(normale_center_object.location) / 1000.0
    
    # Is marble still in cup?
    is_marble_contained = math.sqrt(marble_pos[0] ** 2 + marble_pos[1] ** 2) < 20.0 / 1000.0
    print("Frame #" + str(current_frame) + " contained? " + str(is_marble_contained) + " distance: " + str(math.sqrt(marble_pos[0] ** 2 + marble_pos[1] ** 2)))
    # If marble is not is cup, then there is no normale
    unit_normale = get_unit_normale(normale_edge, marble_pos) if is_marble_contained else mu.Vector()

    # Correction of speed orientation if needed
    rotated_speed = get_rotated_speed(unit_normale, prev_normale, marble_vit) if is_marble_contained else marble_vit
    
    marble_accel = forces_accel_on_marble(rotated_speed, unit_normale, is_marble_contained) - frame_accel
    print(" Acceleration: " + str(marble_accel))

    # Position / velocity update    
    new_marble_pos = update_new_pos(timestep, marble_pos, rotated_speed, marble_accel, normale_edge, is_marble_contained)   
    
    # Test
    new_vit = update_new_vit(timestep, rotated_speed, marble_accel)
    
    print("")
    # Return as mm
    return new_marble_pos*1000.0, new_vit, unit_normale    
