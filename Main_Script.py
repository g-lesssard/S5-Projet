import bpy
import sys
import os
import mathutils as mu

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Forces_acceleration
# from pyquaternion import quaternion

import imp
imp.reload(Forces_acceleration)

# this is optional and allows you to call the functions without specifying the package name
from Forces_acceleration import *
    
bpy.data.objects["Cube"].location = mu.Vector((0.0, 0.0, 0.026499999687075615))
ob_Sphere_location = bpy.data.objects["Sphere"].location
ob_Marble = bpy.data.objects["Marble"]
ob_Marble_rotation = ob_Marble.rotation_quaternion
ob_Marble.animation_data_clear()

marble_pos_path, marble_rot_path = marble_path(750, 0.01, mu.Vector((-0.08877351135015488, 0.1223556399345398, 0.10707605361938477)), mu.Vector((-0.35,-0.58,0)), ob_Sphere_location, ob_Marble_rotation)

marble_pos_path2, marble_rot_path2 = marble_path(400, 0.01, marble_pos_path[-1], mu.Vector((-0.75,-0.6,0)), ob_Sphere_location, marble_rot_path[-1])
frame_num = 0

for position in marble_pos_path + marble_pos_path2:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.location = position
    if frame_num % 2 == 0:
        ob_Marble.keyframe_insert(data_path="location", index = -1)
    frame_num += 1  
    
frame_num = 0 
ob_Marble.rotation_mode = 'QUATERNION'
for rotation in marble_rot_path + marble_rot_path2:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.rotation_quaternion = rotation
    if frame_num % 2 == 0:
        ob_Marble.keyframe_insert(data_path="rotation_quaternion", index = -1)
    frame_num += 1