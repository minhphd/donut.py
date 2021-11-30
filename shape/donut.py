from math import pi
from scipy.spatial.transform import Rotation as R
import numpy as np

axis_x, axis_y, axis_z = (np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1]))

def vector_rotate(vec, angle, axis):
    rotation_vector = axis * angle
    rotation = R.from_rotvec(rotation_vector)
    return rotation.apply(vec)

def draw_donut(R1, R2, init_r):
    dic = {}
    theta_arr = np.arange(0, 2*pi, 0.18).tolist()
    circle = []
    surface_normal = []
    i = 0
    # draw the initial circle
    for theta in theta_arr:
        r0 = [1,0,0]
        norm_r = vector_rotate(r0, theta, axis_z)
        r = init_r + axis_x * (R1 + R2) + norm_r * R2
        circle.append(r)
        surface_normal.append(norm_r)

    # rotate the circle around an axis to create the torus
    for idx, point in enumerate(circle):
        for theta in theta_arr:
            n0 = surface_normal[idx]
            r = init_r + vector_rotate(-point + init_r, theta, axis_y)
            n = vector_rotate(n0, theta, axis_y)
            dic[i] = {"coord": r, "n": n}
            i += 1

    return dic, i