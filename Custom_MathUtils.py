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

# yaw (Z), pitch (Y), roll (X)
def ToQuaternion(yaw, pitch, roll):
    # Abbreviations for the various angular functions
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    w = cy * cp * cr + sy * sp * sr
    x = cy * cp * sr - sy * sp * cr
    y = sy * cp * sr + cy * sp * cr
    z = sy * cp * cr - cy * sp * sr

    return mu.Quaternion((w, x, y, z)).normalized()

def QMul(q1, q2):
    x =  q1.x * q2.w + q1.y * q2.z - q1.z * q2.y + q1.w * q2.x;
    y = -q1.x * q2.z + q1.y * q2.w + q1.z * q2.x + q1.w * q2.y;
    z =  q1.x * q2.y - q1.y * q2.x + q1.z * q2.w + q1.w * q2.z;
    w = -q1.x * q2.x - q1.y * q2.y - q1.z * q2.z + q1.w * q2.w;
    
    return mu.Quaternion((w, x, y, z))