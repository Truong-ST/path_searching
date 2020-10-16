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
    canvas.create_rectangle(position[0] * block+margin, position[1] * block+margin, (position[0]+1) * block+margin-5,
                            (position[1]+1) * block+margin-5,
                            fill=color)


def set_map(size_map):
    for i in range(size_map[0]):
        for j in range(size_map[1]):
            canvas.create_rectangle(j * block+margin, i * block+margin, j * block+margin+25, i * block+margin+25,
                                    fill='black')


def to_position(current_coordinate):
    # reverse
    x = (current_coordinate[0]-margin) // block
    y = (current_coordinate[1]-margin) // block
    return [x, y]

# ------------------------ Set map ---------------------------

set_map(size)
topographic = []
pointer = [0, 0]


def add_pointer():
    x, y = pointer
    topographic.append([x, y])
    print(pointer)

    create_point(pointer, 'blue')
    tk.update_idletasks()
    tk.update()


def get_mouse_coord(event):
    x, y = event.x, event.y

    global pointer
    pointer = to_position([x, y])
    add_pointer()


# def to_move(direct):
#     global pointer
#     if direct == 1:
#         if pointer[1] == 0:
#             return
#
#         pointer[1] += -1
#     elif direct == 3:
#         if pointer[1] == 0:
#             return
#
#         pointer[1] += 1
#     elif direct == 0:
#         if pointer[0] == 0:
#             return
#
#         pointer[0] += 1
#     else:
#         if pointer[0] == 0:
#             return
#
#         pointer[0] += -1
#
#     add_pointer()
def to_up(event):
    global pointer
    if pointer[1] == 0:
        return

    pointer[1] += -1
    add_pointer()


def to_down(event):
    global pointer
    if pointer[1] == 0:
        return

    pointer[1] += 1
    add_pointer()


def to_left(event):
    global pointer
    if pointer[0] == 0:
        return

    pointer[0] += -1
    add_pointer()


def to_right(event):
    global pointer
    if pointer[0] == 0:
        return

    pointer[0] += 1
    add_pointer()


fileCSV = open('map.csv', 'w', newline='')
writer = csv.writer(fileCSV)


def write_file(event):
    writer.writerows(topographic)

    fileCSV.close()
    tk.destroy()


# event
canvas.bind("<Button-1>", get_mouse_coord)
canvas.bind("<Button-3>", write_file)

canvas.bind_all("<KeyPress-Left>", to_left)
canvas.bind_all("<KeyPress-Right>", to_right)
canvas.bind_all("<KeyPress-Up>", to_up)
canvas.bind_all("<KeyPress-Down>", to_down)

tk.mainloop()
