import bpy
import sys
import os
# from vectors import Point, Vector

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

path_test = projectile_path(250, 0.25, Vector(0.0, 0.0, 25.0), Vector(-3.0, 10.0, 20.0))

ob = bpy.data.objects["Sphere"]
ob.animation_data_clear()

frame_num = 0

for position in path_test:
    bpy.context.scene.frame_set(frame_num)
    ob.location = position
    ob.keyframe_insert(data_path="location", index = -1)
    frame_num += 5