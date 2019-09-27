import math
import mathutils as mu

# Math section
def cartesian_to_spherical(cartesian_cs):
    p = math.sqrt(cartesian_cs[0]**2 + cartesian_cs[1]**2 + cartesian_cs[2]**2)
    theta = 0.0
    if (cartesian_cs[0] == 0):
        if (cartesian_cs[1] != 0):
            theta = math.pi/2
    else:
        theta = math.atan(cartesian_cs[1]/cartesian_cs[0])
        
    phi = p if p ==0 else math.acos(cartesian_cs[2]/p) 
    return mu.Vector((p, math.degrees(theta), math.degrees(phi)))

def spherical_to_cartesian(spherical_cs):
    x = spherical_cs[0]*math.cos(math.radians(spherical_cs[1]))*math.sin(math.radians(spherical_cs[2]))
    y = spherical_cs[0]*math.sin(math.radians(spherical_cs[1]))*math.sin(math.radians(spherical_cs[2]))
    z = spherical_cs[0]*math.cos(math.radians(spherical_cs[2]))
    return mu.Vector((x,y,z))