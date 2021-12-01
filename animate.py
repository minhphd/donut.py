from numpy import array, pi, dot
from shape.generator import draw_donut, draw_box, vector_rotate
import curses

rows, cols = (40, 80)

def rendering(terminal):
    axis_x, axis_y, axis_z = (array([1,0,0]), array([0,1,0]), array([0,0,1]))
    init_r = array([cols/2,0,cols/2])
    light = array([0,-1,1])
    R1, R2 = (8,8)
    dic = draw_donut(R1, R2, init_r)
    # dic = draw_box(20, 20, 20, init_r)
    for key in dic.keys():
        r0 = dic[key]["coord"] - init_r
        n0 = dic[key]["n"]
        r = vector_rotate(r0, pi/6, axis_x) + init_r
        n = vector_rotate(n0, pi/6, axis_x)
        dic[key] = {"coord": r, "n": n}
    dtheta = pi/60
    vertical_rot = False
    frames = [2*pi/dtheta, [], []]
    frame_num = 0
    terminal.clear()
    terminal.refresh()
    while frame_num < frames[0]:
        curses.resize_term(rows, cols)
        terminal.clear()
        terminal.border(0)
        for key in dic.keys():
            r0 = dic[key]["coord"]- init_r
            n0 = dic[key]["n"]
            r = vector_rotate(r0, dtheta, axis_z)
            n = vector_rotate(n0, dtheta, axis_z)
            if vertical_rot:
                r = vector_rotate(r, dtheta, axis_x)
                n = vector_rotate(r, dtheta, axis_x)
            r = r + init_r
            dic[key] = {"coord": r,"n": n, "L": dot(n, light)}
        
        values_arr = dic.values()
        Ls = [item['L'] for item in values_arr]
        frames[2].append([min(Ls), max(Ls)])
        # dic = dict(sorted(dic.items(), key=lambda item: item[1]["coord"][1]))
        coords = array([item['coord'] for item in values_arr])
        y_index = {i: {i: [float("-inf"),0] for i in range(cols)} for i in range(rows)}
        for idx, coord in enumerate(coords): 
            x, y, z = coord
            L = Ls[idx]
            if y > y_index[round(z * rows/cols)][round(x)][0]:
                y_index[round(z * rows/cols)][round(x)] = [y, L]
        frames[1].append(y_index)
        string = str(round(frame_num/frames[0] * 100)) + "%"
        terminal.addstr(1,1,string)
        terminal.refresh()
        terminal.move(0,0)
        frame_num += 1

    return frames

def draw(terminal):
    frames = rendering(terminal)
    terminal.clear()
    terminal.refresh()
    terminal.border(0)
    k = 0
    i = 0
    # terminal.nodelay(True)
    string = "render finished, press 's' to view animation"
    terminal.addstr(1,1,string)
    k = terminal.getch()
    if k == ord('s'):
        while True:
            frame = frames[1][i]
            terminal.clear()
            curses.resize_term(rows, cols)
            terminal.border(0)
            scale = ".,-~:;=!*#$@"
            min_illu, max_illu = frames[2][i]
            for row in range(rows):
                for col in range(cols):
                    if frame[row][col] != [float("-inf"),0]:
                        L = frame[row][col][1]
                        scale_index = (L - min_illu) * 11/(max_illu - min_illu)
                        str = scale[round(scale_index)]
                        terminal.addstr(row, col, str)
            if i == len(frames[1]) - 1:
                i = 0
            i += 1
            terminal.timeout(300)
            terminal.move(0,0)
            terminal.refresh()

# draw(0)
if __name__ == "__main__":
    curses.wrapper(draw)
    # draw(0)