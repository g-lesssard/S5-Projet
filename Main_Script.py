import bpy
import sys
import os
import mathutils as mu

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Forces_acceleration

import imp
imp.reload(Forces_acceleration)

# this is optional and allows you to call the functions without specifying the package name
from Forces_acceleration import *
    
ob_Sphere_location = bpy.data.objects["Sphere"].location
ob_Marble = bpy.data.objects["Marble"]
ob_Marble.animation_data_clear()

marble_pos_path = marble_path(200, 0.005, mu.Vector((0,-0.16675525903701782,0.03)), mu.Vector((0,0,0)), ob_Sphere_location)

frame_num = 0

for position in marble_pos_path:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.location = position
    ob_Marble.keyframe_insert(data_path="location", index = -1)
    frame_num += 1  