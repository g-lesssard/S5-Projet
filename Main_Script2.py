import bpy
import sys
import os
import mathutils as muS

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Forces_acceleration2
# from pyquaternion import quaternion

import imp
imp.reload(Forces_acceleration2)

# this is optional and allows you to call the functions without specifying the package name
from Forces_acceleration2 import *
    
centered_pos_marble = mu.Vector((0.0, 0.0, 1.0662171840667725))    
ob_Sphere_location = bpy.data.objects["Substract Volume"].location

ob_Marble = bpy.data.objects["Marble"]
ob_Marble.location = centered_pos_marble
ob_Marble_rotation = ob_Marble.rotation_euler
ob_Marble.animation_data_clear()

marble_pos_path, marble_rot_path = marble_path(750, 0.01, centered_pos_marble/1000, mu.Vector((-0.005,0.0,0)), ob_Sphere_location/1000, ob_Marble_rotation)

frame_num = 0

for position in marble_pos_path:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.location = position*1000
    ob_Marble.keyframe_insert(data_path="location", index = -1)
    frame_num += 1  
    
frame_num = 0 
ob_Marble.rotation_mode = 'QUATERNION'
for rotation in marble_rot_path :
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.rotation_quaternion = rotation
    ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
    frame_num += 1
    
    
ob_Marble.location = centered_pos_marble