import curses
from shape.generator import draw_donut, draw_box, vector_rotate
from numpy import array, pi, dot
import pickle
from datetime import datetime
import os

Running = True
rows, cols = 40, 80
scale = ".,-~:;=!*#$@"

axis_x, axis_y, axis_z = (array([1,0,0]), array([0,1,0]), array([0,0,1]))
init_r = array([cols/2,0,cols/2])
light = array([0,-1,1])

def get_center_pos(title, width, height):
    x = width//2 - (len(title)//2)
    y = height//2
    return int(x), int(y)

def menu(terminal):
    global Running
    option_index = 0
    k = 0
    selected = False

    while True:
        terminal.clear()
        curses.resize_term(rows, cols) 
        terminal.border(0)
        
        if k == ord('w'):
            if option_index > 0:
                option_index -= 1
        elif k == ord('s'):
            if option_index < 3:
                option_index += 1
        elif k == ord('d'):
            selected = True

        if selected:
            if option_index == 0:
                return render(terminal, "donut")
            if option_index == 1:
                return render(terminal, "box")
            if option_index == 2:
                return select_save_file(terminal)
            if option_index == 3:
                selected = False
                Running = False
                return

        # options
        option1 = "render new donut animation"[:cols - 1]
        option2 = "render new box animation"[:cols - 1]
        option3 = "run save files"[:cols - 1]
        option4 = "exit program"[:cols - 1]

        options = [option1, option2, option3, option4]        

        terminal.attron(curses.color_pair(1))
        terminal.attron(curses.A_STANDOUT)

        terminal.addstr(option_index + 1,1, options[option_index])

        terminal.attroff(curses.color_pair(1))
        terminal.attroff(curses.A_STANDOUT)

        for i in range( 4 ):
            if i != option_index:
                terminal.addstr(i + 1,1, options[i])

        k = terminal.getch()

def select_save_file(terminal):
    global Running
    option_index = 0
    k = 0
    selected = False

    while True:
        terminal.clear()
        curses.resize_term(rows, cols) 
        terminal.border(0)

        # options
        options = os.listdir("save-files/")

        if k == ord('w'):
            if option_index > 0:
                option_index -= 1
        elif k == ord('s'):
            if option_index < len(options)-1:
                option_index += 1
        elif k == ord('d'):
            selected = True

        if selected:
            return run_saved(terminal, f"save-files/{options[option_index]}")
        
        terminal.attron(curses.color_pair(1))
        terminal.attron(curses.A_STANDOUT)

        terminal.addstr(option_index + 1,1, options[option_index])

        terminal.attroff(curses.color_pair(1))
        terminal.attroff(curses.A_STANDOUT)

        for i in range( len(options) ):
            if i != option_index:
                terminal.addstr(i + 1,1, options[i])

        k = terminal.getch()

def render(terminal, type):
    k = 0
    selected = False
    if type == "donut":
        dic = draw_donut(8,8,init_r)
    if type == "box":
        dic = draw_box(20,20, 20,init_r)
    
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
        maxmin_illu = [min(Ls), max(Ls)]
        frames[2].append(maxmin_illu)
        coords = array([item['coord'] for item in values_arr])
        y_index = {i: {i: [float("-inf"),0] for i in range(cols)} for i in range(rows)}
        for idx, coord in enumerate(coords): 
            x, y, z = coord
            L = Ls[idx]
            if y > y_index[round(z * rows/cols)][round(x)][0]:
                y_index[round(z * rows/cols)][round(x)] = [y, L]

        min_illu, max_illu = maxmin_illu        
        for row in range(rows):
            for col in range(cols):
                if y_index[row][col] != [float("-inf"),0]:
                    L = y_index[row][col][1]
                    scale_index = (L - min_illu) * 11/(max_illu - min_illu)
                    string = scale[round(scale_index)]
                    terminal.addstr(row, col, string)

        frames[1].append(y_index)
        string = str(round(frame_num/frames[0] * 100)) + "%"
        terminal.addstr(rows-1,1,string)
        terminal.refresh()
        terminal.move(0,0)
        frame_num += 1

    option = 0
    terminal.nodelay(False)

    filename = f'save-files/{type}-{datetime.today().strftime("%Y%m%dT%H%M%S%z")}'
    outfile = open(filename, 'wb')
    pickle.dump(frames, outfile)
    outfile.close()

    while True:
        curses.resize_term(rows, cols)
        terminal.clear()
        terminal.border(0)
        
        if k == ord('w'):
            if option > 0:
                    option -= 1
        elif k == ord('s'):
            if option < 1:
                option += 1
        elif k == ord('d'):
            selected = True

        if selected:
            if option == 0:
                return run_saved(terminal, filename)
            if option == 1:
                selected = False
                return 

        #to be updated
        title = "Animation is rendered and saved in save file folder"[:cols-1]
        option1 = "play animation"[:cols-1]
        option2 = "return to menu"[:cols-1]
        options = [option1, option2]

        x, y = get_center_pos(title, cols, rows) 
        terminal.addstr(y-1, x, title)
        
        terminal.attron(curses.A_STANDOUT)
        terminal.attron(curses.color_pair(1))
        x, y = get_center_pos(options[option], cols, rows)
        terminal.addstr(y+option, x, options[option])
        terminal.attroff(curses.A_STANDOUT)
        terminal.attroff(curses.color_pair(1))

        x, y = get_center_pos(options[len(options)-1-option], cols, rows)
        terminal.addstr(y+len(options)-1-option, x, options[len(options)-1-option])
        terminal.addstr(1,1,str(option))
        k = terminal.getch()
        terminal.refresh()
        terminal.move(0,0)

def run_saved(terminal, filename):
    file = open(filename, "rb")
    frames = pickle.load(file, encoding='bytes')
    file.close()
    terminal.clear()
    terminal.refresh()
    terminal.border(0)
    k = 0
    i = 0
    terminal.nodelay(True)
    while True:
        if k == ord('q'):
            return    
        frame = frames[1][i]
        terminal.clear()
        curses.resize_term(rows, cols)
        terminal.border(0)
        scale = ".,-~:;=!*#$@"
        min_illu, max_illu = frames[2][i]
        title = "press 'q' to return to menu"
        x, y = get_center_pos(title, cols, rows)
        terminal.addstr(rows - 3, x, title)
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

        k = terminal.getch()
        terminal.timeout(50)
        terminal.move(0,0)
        terminal.refresh()

def draw(terminal):
    global Running
    terminal.clear()
    terminal.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while Running:
       menu(terminal)

if __name__ == "__main__":
    curses.wrapper(draw)