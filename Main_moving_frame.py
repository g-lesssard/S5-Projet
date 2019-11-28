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
    
Initiale_Marble_Pos = mu.Vector((0.0, 0.0, 1.0662171840667725))    
ob_Sphere = bpy.data.objects["Substract Volume"]

ob_Marble = bpy.data.objects["Marble"]
ob_Marble.location = Initiale_Marble_Pos
ob_Marble_rotation = ob_Marble.rotation_euler
ob_Marble.animation_data_clear()

animation_length = 250

frame_num = 0

bpy.context.scene.frame_set(frame_num)

frame_marble(ob_Sphere, 0.1, ob_Marble.location, mu.Vector())

#For testing purpose only
position = ob_Marble.location
vit = mu.Vector((1.0, 1.0, 1.0))
accel = mu.Vector((1.0, 1.0, 1.0))
for i in range(0,2):
    position, vit, accel = frame_marble(ob_Sphere, 0.1, position, vit, accel)     

#for position in marble_pos_path:
#    bpy.context.scene.frame_set(frame_num)
#    ob_Marble.location = position*1000
#    ob_Marble.keyframe_insert(data_path="location", index = -1)
#    frame_num += 1  
    
#frame_num = 0 
#ob_Marble.rotation_mode = 'QUATERNION'
#for rotation in marble_rot_path :
#    bpy.context.scene.frame_set(frame_num)
#    ob_Marble.rotation_quaternion = rotation
#    ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
#    frame_num += 1