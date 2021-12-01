from scipy.spatial.transform import Rotation as R
import numpy as np
from shape.generator import draw_donut, draw_box, vector_rotate
import curses

pi = np.pi
rows, cols = (40, 80)
scale = ".,-~:;=!*#$@"
R1, R2 = (6,6)
axis_x, axis_y, axis_z = (np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1]))
init_r = np.array([cols/2,0,cols/2])
dic, i = draw_donut(R1, R2, init_r)
# dic, i = draw_box(15,15,30,init_r)
light = np.array([0,-1,1])

# # animate
for idx in range(i):
    r0 = dic[idx]["coord"] - init_r
    n0 = dic[idx]["n"]
    r = vector_rotate(r0, pi/6, axis_x) + init_r
    n = vector_rotate(n0, pi/6, axis_x)
    dic[idx] = {"coord": r, "n": n}

def draw(terminal):
    terminal.clear()
    terminal.refresh()
    theta = 0
    k = 0
    terminal.nodelay(True)
    while k != ord('q'):
        points = []
        shade = []
        k = terminal.getch()
        for idx in range(i):
            r0 = dic[idx]["coord"]- init_r
            n0 = dic[idx]["n"]
            r = vector_rotate(r0, theta, axis_z) + init_r
            n = vector_rotate(n0, theta, axis_z)
            points.append(r.tolist())
            shade.append(np.dot(n, light))

        terminal.clear()
        curses.resize_term(rows, cols)
        terminal.border(0)
        shade = [x for _, x in sorted(zip(points, shade), key=lambda pair: pair[0][1])]
        points.sort(key=lambda x: x[1])
        min_illu, max_illu  = min(shade), max(shade)
        for idx in range(i):
            x, y, z = points[idx]
            illu = (shade[idx] - min_illu)*11/(max_illu - min_illu)
            string = scale[round(illu)]
            terminal.addstr(round(z * rows/cols), round(x), string, curses.A_BOLD)
        theta += 0.05
        terminal.move(0,0)
        terminal.refresh()


curses.wrapper(draw)