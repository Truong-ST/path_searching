from tkinter import *
import numpy as np
import time

from a_star_searching import AStarSearching
from utilities import *


config_dict = set_configuration()

width = config_dict['width']
height = config_dict['height']
block = config_dict['block']
margin = config_dict['margin']
size = (20, 20)

tk = Tk()
tk.title('Illustration')
canvas = Canvas(tk, width=width, height=height)
tk.resizable(0, 0)
canvas.pack()


def draw_map(size):
    for row in range(size[0]):
        for col in range(size[1]):
            canvas.create_rectangle(col * block+margin, row * block+margin, col * block+margin+4,
                                    row * block+margin+4, fill='black')


def create_point(position, size, color):
    canvas.create_rectangle(position[0], position[1], position[0]+size, position[1]+size, fill=color)


draw_map(size)
start = [1, 0]
goal = [17, 16]

as_path = AStarSearching(size,
                         start,
                         goal)

# set topographic
mark = get_topographic('map.csv')
for pos in mark:
    as_path.mark[pos[1]][pos[0]] = 2

topographic = []
for row in range(len(as_path.mark)):
    for col in range(len(as_path.mark[0])):
        if as_path.mark[row][col] == 2:
            topographic.append([row, col])
# print(topographic)

path = as_path.a_star()
print(path)

real_topographic = scale_coordinate(topographic, block, margin)
min_path = scale_coordinate(path, block, margin)

# ----------------------- Draw ------------------------

# draw map
t = 0
timer = canvas.create_text(width-30, 15, text='0')
start_end = scale_coordinate([start, goal], block, margin)

for point in start_end:
    create_point(point, 10, 'red')

for pos_rock in real_topographic:
    create_point(pos_rock, 20, 'gray')

tk.update()
time.sleep(1.5)

# Draw finding path process
for step in as_path.process:
    scale_step = scale_coordinate(step, block, margin)

    t += 0.2
    canvas.itemconfigure(timer, text=str(round(t, 2)))

    create_point(scale_step[0], 10, 'green')
    current_point = canvas.create_rectangle(scale_step[0][0], scale_step[0][1], scale_step[0][0]+10,
                                            scale_step[0][1]+10, fill='cyan')

    for i in range(1, len(step)):
        create_point(scale_step[i], 10, 'yellow')

    time.sleep(0.2)
    tk.update()

    canvas.delete(current_point)

# Draw min path
for pos in min_path:
    time.sleep(0.15)
    create_point(pos, 10, 'red')

    tk.update()

tk.mainloop()
