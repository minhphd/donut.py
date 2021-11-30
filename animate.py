from math import pi
from scipy.spatial.transform import Rotation as R
import numpy as np
from shape.donut import draw_donut
import curses

rows, cols = (40, 80)
scale = ".,-~:;=!*#$@"
R1, R2 = (6,6)
axis_x, axis_y, axis_z = (np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1]))
init_r = np.array([cols/2,0,cols/2])
dic, i = draw_donut(R1, R2, init_r)
light = np.array([0,-1,1])

def vector_rotate(vec, angle, axis):
    rotation_vector = axis * angle
    rotation = R.from_rotvec(rotation_vector)
    return rotation.apply(vec)

# # animate
for idx in range(i):
    r0 = dic[idx]["coord"] - init_r
    n0 = dic[idx]["n"]
    r = vector_rotate(r0, -pi/6, axis_x) + init_r
    n = vector_rotate(n0, -pi/6, axis_x)
    dic[idx] = {"coord": r, "n": n}

def draw(terminal):

    terminal.clear()
    terminal.refresh()
    theta = 0
    k = 0
    terminal.nodelay(True)
    while k != ord('q'):
        new_dic = {}
        shade = []
        k = terminal.getch()
        for idx in range(i):
            r0 = dic[idx]["coord"]- init_r
            n0 = dic[idx]["n"]
            r = vector_rotate(r0, theta, axis_z) + init_r
            n = vector_rotate(n0, theta, axis_z)
            new_dic[idx] = {"coord": r, "n": n}
            shade.append(np.dot(n, light))

        terminal.clear()
        curses.resize_term(rows, cols)
        terminal.border(0)
        min_illu = min(shade)
        max_illu = max(shade)
        for idx in range(i):
            x, y, z = new_dic[idx]["coord"].tolist()
            illu = (shade[idx] - min_illu)*11/(max_illu - min_illu)
            string = scale[round(illu)]
            terminal.addstr(round(z * rows/cols), round(x), string, curses.A_BOLD)
        theta += 0.05
        terminal.refresh()


curses.wrapper(draw)