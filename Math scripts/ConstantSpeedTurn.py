import numpy as np


def max_velocity_constant_turn(angular_velocity, turn_radius):
    R = 68.17
    delta_x = 20
    g = 9.81

    theta = np.arcsin(delta_x/R)
    delta_z = R - R*np.cos(theta)

    phi = np.arctan(delta_x/delta_z)

    angular_velocity_z = angular_velocity/np.cos(np.pi/2 - phi)

    return np.pi


max_velocity_constant_turn(10,30)