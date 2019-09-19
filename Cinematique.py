import math
import numpy as np

def cinematique_position(current_time, init_p = 0.0, init_s = 0.0, init_a = -9.806):
    return init_p + init_s * current_time + 0.5 * init_a * current_time ** 2
    
def cinematique_speed(current_time, init_s = 0.0, init_a = -9.806):
    return init_s + init_a * current_time

# Collision section, m in kg and v in m/s
# initial masses are at 2 kg by default so 1/m1 + 1/m2 would be 1 by default
def collision3D(speed1, e = 1.0, normale = np.array([0,0,1]), speed2 = np.array([0,0,0]), m1 = 2.0, m2 = 2.0):
    p = (1 + e) * speed1.dot(normale) * (normale) / (1/m1 + 1/m2)
    return ((speed1 - p), (speed2 + p))

# It's important to mention here that timestep aren't binded to keyframes. Logic of correct ratio for 
# keyframes / timestep must be done outside the function.
def projectile_path(iter_nb = 1, timestep = 1, init_p = np.array([0,0,0]), init_s = np.array([0,0,0]), init_a = np.array([0,0,-9.806])):
    pos_path = []
    if iter_nb > 0.0:
        x = cinematique_position(timestep, init_p[0], init_s[0], init_a[0])
        y = cinematique_position(timestep, init_p[1], init_s[1], init_a[1])
        z = cinematique_position(timestep, init_p[2], init_s[2], init_a[2])
        new_pos = np.array([x,y,z])
        
        init_s[0] = cinematique_speed(timestep, init_s[0], init_a[0])
        init_s[1] = cinematique_speed(timestep, init_s[1], init_a[1])
        init_s[2] = cinematique_speed(timestep, init_s[2], init_a[2])                
        
        # hardcoded to collide with floor only here
        # for now there is an undesirable offset
        if (z <= 5):
            init_s = collision3D(init_s, 0.7)[0]
        pos_path.append(new_pos)        
        iter_nb -= 1
        for pos in projectile_path(iter_nb, timestep, new_pos, init_s):
            pos_path.append(pos)
    return pos_path

def speed_after_collision(m1, v1, m2, v2, e, normale):
    return (m1*v1+m2*(v2-e*(v1-v2)))/(m1+m2)

# Math section
def cartesian_to_spherical(cartesian_cs):
    p = math.sqrt(cartesian_cs[0]**2, cartesian_cs[1]**2, cartesian_cs[2]**2)
    theta = 0.0
    if (cartesian_cs[0] == 0):
        if (cartesian_cs[1] != 0):
            theta = math.pi/2
    else:
        theta = math.atan(cartesian_cs[1]/cartesian_cs[0])
    phi = math.acos(cartesian_cs[2]/p) 
    return (p, theta, phi)

def spherical_to_cartesian(spherical_cs):
    x = spherical_cs[0]*math.cos(spherical_cs[1])*math.sin(spherical_cs[2])
    y = spherical_cs[0]*math.sin(spherical_cs[1])*math.sin(spherical_cs[2])
    z = spherical_cs[0]*math.cos(spherical_cs[2])
    return (x,y,z)

# Forces section

def gravity_force(m):
    return m*(0,0,-9.8)

     # normal must be in unit form
def normal_force(g_force, normal_direction = (0,0,1)):
    spherical_normal = cartesian_to_spherical(normal_direction)
    return g_force*math.cos(spherical_normal[1])*normal_direction

