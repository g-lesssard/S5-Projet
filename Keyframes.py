import bpy
import bmesh
import sys
import os
import mathutils as mu
import math

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Cinematique

# this next part forces a reload in case you edit the source after you first start the blender session
import imp
imp.reload(Cinematique)

# this is optional and allows you to call the functions without specifying the package name
from Cinematique import *

# Keyframe inserter

testest = collision3D(mu.Vector((0, 24*math.cos(math.radians(60)), -24*math.sin(math.radians(60)))), 0.8, mu.Vector((0,0,1)))
print(str(testest[0]))
print(str(testest[0].normalize()))

path_test = projectile_path(400, 0.5, mu.Vector((5.0, 5.0, 10.0)), mu.Vector((-5, 3, 60.0)))

ob = bpy.data.objects["Sphere"]
ob.animation_data_clear()

frame_num = 0

for position in path_test:
    bpy.context.scene.frame_set(frame_num)
    ob.location = position
    ob.keyframe_insert(data_path="location", index = -1)
    frame_num += 1  