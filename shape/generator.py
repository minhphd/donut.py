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
    theta_arr = np.arange(0, 2*pi + 0.1, 0.1).tolist()
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


def draw_box(w, l, h, init_r):
    width = np.arange(-w/2, w/2 + 1, 1)
    length = np.arange(-l/2, l/2 + 1, 1)
    height = np.arange(-h/2, h/2 + 1, 1)
    dic = {}
    i = 0
    for x in width:
        for y in length:
            r = init_r + np.array([x, y, -h/2])
            n = np.array([0,0,-1])
            dic[i] = {"coord": r, "n": n}
            i += 1

    count = 0

    for j in range(0, i, 1):
        x0, y0, z0 = (dic[j]["coord"] - init_r).tolist()
        if x0 in {-w/2, w/2} or y0 in {-l/2, l/2}:
            for z in height:
                r = init_r + np.array([x0, y0, z])
                if  -l/2 < y0 < l/2:
                    if x0 == -w/2:
                        n = np.array([-1,0,0])
                    elif x0 == w/2:
                        n = np.array([1,0,0])
                elif  -w/2 < x0 < w/2:
                    if y0 == -l/2:
                        n = np.array([0,-1,0])
                    elif y0 == l/2:
                        n = np.array([0,1,0])
                dic[i] = {"coord": r, "n": n}
                i += 1
        # else:
        r = init_r + np.array([x0, y0, -z0])
        n = np.array([0,0,1])
        dic[i] = {"coord": r, "n": n}
        i += 1

    return dic, i
