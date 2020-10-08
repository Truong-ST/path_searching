from tkinter import *
import csv

from utilities import set_configuration


config_dict = set_configuration()

width = config_dict['width']
height = config_dict['height']
block = config_dict['block']
margin = config_dict['margin']
size = (20, 20)

tk = Tk()
tk.title('set map')
canvas = Canvas(tk, bg='light green', width=width, height=height)
tk.resizable(0, 0)
canvas.pack()


def create_point(position, color):
    canvas.create_rectangle(position[0] * block+margin, position[1] * block+margin, position[0] * block+margin+25,
                            position[1] * block+margin+25,
                            fill=color)


def set_map(size_map):
    for i in range(size_map[0]):
        for j in range(size_map[1]):
            canvas.create_rectangle(j * block+margin, i * block+margin, j * block+margin+25, i * block+margin+25,
                                    fill='black')


def to_position(lis):
    # reverse
    x = (lis[0]-margin) // block
    y = (lis[1]-margin) // block
    return [x, y]


set_map(size)
topographic = []


def get_mouse_coord(event):
    x, y = event.x, event.y
    create_point(to_position([x, y]), 'blue')
    topographic.append(to_position([x, y]))
    print(to_position([x, y]))

    tk.update_idletasks()
    tk.update()


fileCSV = open('map.csv', 'w', newline='')
writer = csv.writer(fileCSV)


def write_file(event):
    writer.writerows(topographic)
    fileCSV.close()
    tk.destroy()


canvas.bind("<Button-1>", get_mouse_coord)
canvas.bind("<Button-3>", write_file)

tk.mainloop()
