import bpy
import sys
import os
import mathutils as muS

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
    
initiale_marble_pos = mu.Vector((0.0, 0.0, 10.619390487670898))  
test_marble_pos = mu.Vector((-11.0892972946167, 0.0, 11.624490737915039))
initiale_carFrame_pos = mu.Vector((0.0, 0.0, 2.5))  
ob_Sphere = bpy.data.objects["Substract Volume"]
ob_CarFrame = bpy.data.objects["CarFrame"]

ob_Marble = bpy.data.objects["Marble"]
ob_Marble.location = initiale_marble_pos
ob_Marble_rotation = ob_Marble.rotation_euler
ob_Marble.animation_data_clear()

animation_length = 24

frame_num = 0

bpy.context.scene.frame_set(frame_num)

# temp to set at start
set_location_at_keyframe(ob_Marble, 0, initiale_marble_pos)
#set_location_at_keyframe(ob_Marble, 0, test_marble_pos)

#set_location_at_keyframe(ob_CarFrame, 0, initiale_carFrame_pos)

#For testing purpose only
position = ob_Marble.location
vit = mu.Vector((0.0, 0.0, 0.0))
unit_normale = get_unit_normale(ob_Sphere.location, position)
timestep = 1.0/30.0 #we are currently at 60 fps
for frame_number in range(1,animation_length):
    position, vit, unit_normale = frame_marble(ob_Sphere, timestep, position, vit, unit_normale, frame_number)     
    set_location_at_keyframe(ob_Marble, frame_number, position)  
    
#frame_num = 0 
#ob_Marble.rotation_mode = 'QUATERNION'
#for rotation in marble_rot_path :
#    bpy.context.scene.frame_set(frame_num)
#    ob_Marble.rotation_quaternion = rotation
#    ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
#    frame_num += 1