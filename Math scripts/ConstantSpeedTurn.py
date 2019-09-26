import numpy as np
import matplotlib.pyplot as mplt


def max_velocity_constant_turn(turn_radius):
    R = 68.17/1000
    delta_x = 20/1000
    g = 9.81
    w_z = np.sqrt(g/turn_radius)

    theta = np.arcsin(delta_x/R)
    delta_z = R - R*np.cos(theta)

    phi = np.arctan(delta_x/delta_z)

    angular_velocity = w_z / np.sin(np.pi/2 - phi)

    return turn_radius * angular_velocity


# Testing
number_of_points = 1000
turn_radi = list(np.linspace(0, 2, number_of_points))
speeds = np.empty(number_of_points)

for turn_radius in turn_radi:
    if turn_radius != 0:
        i = turn_radi.index(turn_radius)
        speeds[i] = max_velocity_constant_turn(turn_radius=turn_radius)


mplt.stem(turn_radi, speeds)
mplt.show()
