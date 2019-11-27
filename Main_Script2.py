import bpy
import sys
import os
import mathutils as muS

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Forces_acceleration
# from pyquaternion import quaternion

import imp
imp.reload(Forces_acceleration)

# this is optional and allows you to call the functions without specifying the package name
from Forces_acceleration import *
    
centered_pos_marble = mu.Vector((0.0, 0.0, 1.0662171840667725))    
ob_Sphere_location = bpy.data.objects["Substract Volume"].location

ob_Marble = bpy.data.objects["Marble"]
ob_Marble.location = centered_pos_marble
ob_Marble_rotation = ob_Marble.rotation_euler
ob_Marble.animation_data_clear()

marble_pos_path, marble_rot_path = marble_path(750, 0.01, centered_pos_marble, mu.Vector((-3.5,-5.8,0)), ob_Sphere_location, ob_Marble_rotation)

marble_pos_path2, marble_rot_path2 = marble_path(400, 0.01, marble_pos_path[-1], mu.Vector((-7.5,-6.0,0)), ob_Sphere_location, marble_rot_path[-1].to_euler())
frame_num = 0

for position in marble_pos_path + marble_pos_path2:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.location = position
    ob_Marble.keyframe_insert(data_path="location", index = -1)
    frame_num += 1  
    
frame_num = 0 
ob_Marble.rotation_mode = 'QUATERNION'
for rotation in marble_rot_path + marble_rot_path2:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.rotation_quaternion = rotation
    ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
    frame_num += 1