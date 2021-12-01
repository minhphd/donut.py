from numpy import array, pi, dot
from shape.generator import draw_donut, draw_box, vector_rotate
import curses


def draw(terminal):
    rows, cols = (40, 80)
    scale = ".,-~:;=!*#$@"
    axis_x, axis_y, axis_z = (array([1,0,0]), array([0,1,0]), array([0,0,1]))
    init_r = array([cols/2,0,cols/2])
    light = array([0,-1,1])
    R1, R2 = (6,6)
    dic = draw_donut(R1, R2, init_r)
    # dic = draw_box(15, 15, 30, init_r)
    for key in dic.keys():
        r0 = dic[key]["coord"] - init_r
        n0 = dic[key]["n"]
        r = vector_rotate(r0, pi/6, axis_x) + init_r
        n = vector_rotate(n0, pi/6, axis_x)
        dic[key] = {"coord": r, "n": n}
    terminal.clear()
    terminal.refresh()
    dtheta = pi/50
    k = 0
    terminal.nodelay(True)
    while k != ord('q'):
        k = terminal.getch()
        for key in dic.keys():
            r0 = dic[key]["coord"]- init_r
            n0 = dic[key]["n"]
            r = vector_rotate(r0, dtheta, axis_z) + init_r
            n = vector_rotate(n0, dtheta, axis_z)
            dic[key] = {"coord": r,"n": n, "L": dot(n, light)}

        dic = dict(sorted(dic.items(), key=lambda item: item[1]["coord"][1]))

        terminal.clear()
        curses.resize_term(rows, cols)
        terminal.border(0)
        values_arr = [item['L'] for item in dic.values()]
        min_illu, max_illu  = min(values_arr), max(values_arr)
        for key in dic.keys():
            x, y, z = dic[key]["coord"]
            L = dic[key]["L"]
            illu = (L - min_illu)*11/(max_illu - min_illu)
            string = scale[round(illu)]
            terminal.addstr(round(z * rows/cols), round(x), string, curses.A_BOLD)
        terminal.move(0,0)
        terminal.refresh()


# draw(0)
if __name__ == "__main__":
    curses.wrapper(draw)