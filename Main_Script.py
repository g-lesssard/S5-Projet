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
ob_Marble.animation_data_clear()

marble_pos_path = marble_path(5*612, 0.0025, mu.Vector((-0.09409496188163757, 0.1060512512922287, 0.10304122418165207)), mu.Vector((0.38,-0.123,0)), ob_Sphere_location)

frame_num = 0

for position in marble_pos_path:
    bpy.context.scene.frame_set(frame_num)
    ob_Marble.location = position
    ob_Marble.keyframe_insert(data_path="location", index = -1)
    frame_num += 0.25  