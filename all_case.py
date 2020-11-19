from tkinter import *
import numpy as np
import time
import math

from a_star_searching import AStarSearching
from utilities import *


config_dict = set_configuration('configuration.yaml')
width = config_dict['width']
height = config_dict['height']
block = config_dict['block']
margin = config_dict['margin']
width = 1400
height = 750

tk = Tk()
tk.title('Illustration')
canvas = Canvas(tk, width=width, height=height, scrollregion=(0, 0, 8000, 1600))
tk.resizable(0, 0)
hbar = Scrollbar(tk, orient=HORIZONTAL)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=canvas.xview)

vbar = Scrollbar(tk, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack()
# canvas.pack(side=LEFT, expand=True, fill=BOTH)

r = 28
rotate = np.array([[0, 1], [-1, 0]])
size = (30, 30)


def create_point(position, size, color):
    canvas.create_rectangle(position[0], position[1], position[0]+size, position[1]+size, fill=color)



def create_infor(position, text):
    canvas.create_text(position[0], position[1], text=text)
    return canvas.create_text(position[0] + 50, position[1], text='null')


def create_full(pos, theta, color_left, color_right):
    st = np.array([math.cos(theta), math.sin(theta)])
    vector_rotate = rotate.dot(st * r / np.linalg.norm(st))
    center = pos

    left = np.array(center) + vector_rotate
    right = np.array(center) - vector_rotate
    canvas.create_oval(left[0]-r, left[1]-r, left[0]+r, left[1]+r, outline=color_left, width=2)
    canvas.create_oval(right[0]-r, right[1]-r, right[0]+r, right[1]+r, outline=color_right, width=2)
    vector = pos + 20*st
    canvas.create_line(*pos, *vector, fill='black', arrow=LAST)

cell = 170
margin = 80

for i in range(5):
    d = 20 * i
    for j in range(5):
        anpha = j * math.pi / 4 - math.pi / 2
        for k in range(8):
            origin = np.array([(j*8+k)*cell+margin, i*cell+margin])
            pos = origin + d * np.array([math.cos(anpha), math.sin(anpha)])
            theta_goal = k * math.pi / 4 - math.pi / 2
            create_full(origin, -math.pi / 2, 'blue', 'green')
            create_point(origin, 5, 'red')
            create_full(pos, theta_goal, 'royalblue', 'springgreen3')
            create_point(pos, 5, 'yellow')

for i in range(1, 6):
    canvas.create_line(i*8*cell+margin-75, 0, i*8*cell+margin-75, height*2)

tk.update()
tk.mainloop()