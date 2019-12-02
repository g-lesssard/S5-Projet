import bpy
import sys
import os
import mathutils as mu
import math

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import forces_and_accelerations
# from pyquaternion import quaternion

import imp
imp.reload(forces_and_accelerations)

# this is optional and allows you to call the functions without specifying the package name
from forces_and_accelerations import *

def set_location_at_keyframe(object, frame_number, location):
    bpy.context.scene.frame_set(frame_number)
    object.location = location
    object.keyframe_insert(data_path="location", index = -1)     
    
def update_scene():
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()   
    
# Position to be at right height and centered with the car framne
initiale_marble_pos = mu.Vector((0.0, 0.0, 8.119390487670898))  
# Is still viable?
test_marble_pos = mu.Vector((-11.0892972946167, 0.0, 11.624490737915039))
initiale_carFrame_pos = mu.Vector((0.0, 0.0, 2.5))  
ob_Sphere = bpy.data.objects["Substract Volume"]
ob_CarFrame = bpy.data.objects["CarFrame"]

ob_Marble = bpy.data.objects["Marble"]
ob_Marble.location = initiale_marble_pos
ob_Marble_rotation = ob_Marble.rotation_euler
ob_Marble.animation_data_clear()

frame_num = 0

bpy.context.scene.frame_set(frame_num)

ob_car_path = bpy.data.objects["Car_Path1"]
ob_CarFrame.parent = ob_car_path
update_scene()

# Take path eval time as animation length
animation_length = ob_car_path.data.path_duration
# Set scene animation length to path animation length value
bpy.context.scene.frame_end = animation_length

# temp to set at start
set_location_at_keyframe(ob_Marble, 0, initiale_marble_pos + get_global_co(ob_CarFrame))
#set_location_at_keyframe(ob_Marble, 0, test_marble_pos)

#For testing purpose only
position = ob_Marble.location
vit = mu.Vector((0.0, 0.0, 0.0))
unit_normale = get_unit_normale(get_global_co(ob_Sphere), position)

# Get framerate
framerate = bpy.context.scene.render.fps
timestep = 1.0 / framerate 

for frame_number in range(frame_num + 1, frame_num + animation_length):
    position, vit, unit_normale = frame_marble(ob_Sphere, timestep, position, vit, unit_normale, frame_number)     
    set_location_at_keyframe(ob_Marble, frame_number, position)  
    
#frame_num = 0 
#ob_Marble.rotation_mode = 'QUATERNION'
#for rotation in marble_rot_path :
#    bpy.context.scene.frame_set(frame_num)
#    ob_Marble.rotation_quaternion = rotation
#    ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
#    frame_num += 1