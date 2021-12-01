from numpy import asarray, array, linspace, dot
from math import pi, sin, cos, sqrt

axis_x, axis_y, axis_z = (array([1,0,0]), array([0,1,0]), array([0,0,1]))

def rotation_matrix(axis, theta):
    axis = asarray(axis)
    axis = axis / sqrt(dot(axis, axis))
    a = cos(theta / 2.0)
    b, c, d = -axis * sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def vector_rotate(vec, angle, axis):
    M0 = rotation_matrix(axis, angle)
    return dot(M0, vec)

def draw_donut(R1, R2, init_r):
    dic = {}
    theta_arr = linspace(0, 2*pi, 60).tolist()
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

    print(i)
    return dic


def draw_box(w, l, h, init_r):
    width = linspace(-w/2, w/2, 15)
    length = linspace(-l/2, l/2, 15)
    height = linspace(-h/2, h/2, 15)
    dic = {}
    i = 0
    for x in width:
        for y in length:
            r = init_r + array([x, y, -h/2])
            n = array([0,0,-1])
            dic[i] = {"coord": r, "n": n}
            i += 1

    for j in range(0, i, 1):
        x0, y0, z0 = (dic[j]["coord"] - init_r).tolist()
        if x0 in {-w/2, w/2} or y0 in {-l/2, l/2}:
            for z in height:
                r = init_r + array([x0, y0, z])
                if  -l/2 <= y0 < l/2:
                    if x0 == -w/2:
                        n = array([-1,0,0])
                    elif x0 == w/2:
                        n = array([1,0,0])
                elif  -w/2 <= x0 < w/2:
                    if y0 == -l/2:
                        n = array([0,-1,0])
                    elif y0 == l/2:
                        n = array([0,1,0])
                dic[i] = {"coord": r, "n": n}
                i += 1

        else:
            r = init_r + array([x0, y0, h/2])
            n = array([0,0,1])
            dic[i] = {"coord": r, "n": n}
            i += 1
    # print(count)
    return dic


# draw_donut(5,5,np.array([0,0,0]))