import bpy
import mathutils as mu

GRAVITY = 9.807
# Mass in kg
MARBLE_MASS = 4.56/1000

def marble_normal_force(marble_center, sphere_center):
    normal_v = mu.Vector((sphere_center[0]-marble_center[0], sphere_center[1]-marble_center[1], sphere_center[2]-marble_center[2]))
    normal_v.normalize()
    
    print(str(normal_v))