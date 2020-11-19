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

tk = Tk()
tk.title('Illustration')
canvas = Canvas(tk, width=width, height=height)
tk.resizable(0, 0)
canvas.pack()


def draw_map(size):
    for row in range(size[0]):
        for col in range(size[1]):
            if row == 0 or row == size[0] - 1 or col == 0 or col == size[1] - 1:
                canvas.create_rectangle(col * block + margin, row * block + margin, col * block + margin + block,
                                        row * block + margin + block, fill='black')
            canvas.create_rectangle(col * block+margin, row * block+margin, col * block+margin+1,
                                    row * block+margin+1, fill='black')


def create_point(position, size, color):
    canvas.create_rectangle(position[0], position[1], position[0]+size, position[1]+size, fill=color)


def increase_coordinate(pos, bias):
    return [pos[0]+bias, pos[1]+bias]


def create_infor(position, text):
    canvas.create_text(position[0], position[1], text=text)
    return canvas.create_text(position[0] + 50, position[1], text='null')


def predict_s(start, tail_start, goal, tail_goal):
    pass


size = (35, 35)
start = np.array([400, 370])
goal = np.array([200, 360])
theta_goal = math.pi / 2
as_path = AStarSearching(size,
                         start,
                         goal,
                         theta_goal=math.pi / 2,
                         length=40,
                         v=20,
                         theta=0,
                         phi=math.pi / 4)
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
# min_path = scale_coordinate(path, block, margin)


# ----------------------- Draw ------------------------
# Show information
t = 0
canvas.create_text(width-60, 80, text='INFORMATION')
timer = create_infor((width-80, 30), 'Time:')
canvas.create_text(width-100, 100, text='Origin ray: ')
canvas.create_line(width-50, 100, width-20, 100, arrow=LAST)
distance = create_infor((width-100, 130), 'Total S:')

# predict
canvas.create_text(width-80, 250, text='PREDICT ')
# canvas.create_text(width-100, 280, text='Total S:  ' + 'null')

# draw start-goal
r = as_path.r
rotate = np.array([[0, 1], [-1, 0]])
st = np.array(start) - np.array(as_path.process[0][1])
vector_rotate = rotate.dot(st * r / as_path.length)
center = (st / 2 + as_path.process[0][1]).astype(int)

left = np.array(center) + vector_rotate
right = np.array(center) - vector_rotate
canvas.create_oval(left[0]-r, left[1]-r, left[0]+r, left[1]+r, fill='blue')
canvas.create_oval(right[0]-r, right[1]-r, right[0]+r, right[1]+r, fill='green')

create_point(left, 3, 'yellow')
create_point(right, 3, 'yellow')

tail_goal = as_path.get_tail(goal, theta_goal)
gl = np.array(goal) - tail_goal
vector_rotate_goal = rotate.dot(gl * r / as_path.length)
center_goal = (gl / 2 + tail_goal).astype(int)

left_goal = np.array(center_goal) + vector_rotate_goal
right_goal = np.array(center_goal) - vector_rotate_goal
canvas.create_oval(left_goal[0]-r, left_goal[1]-r, left_goal[0]+r, left_goal[1]+r, fill='blue')
canvas.create_oval(right_goal[0]-r, right_goal[1]-r, right_goal[0]+r, right_goal[1]+r, fill='green')

create_point(left_goal, 3, 'yellow')
create_point(right_goal, 3, 'yellow')

create_point(start, 6, 'red')
create_point(goal, 6, 'red')
canvas.create_line(as_path.process[0][1][0], as_path.process[0][1][1], as_path.process[0][0][0], as_path.process[0][0][1], fill='black', width=4, arrow=LAST)
canvas.create_line(tail_goal[0], tail_goal[1], goal[0], goal[1], fill='black', width=4, arrow=LAST)

# choose circle
chosen = as_path.choose_circle(vector_rotate, vector_rotate_goal)
if chosen[0]:
    canvas.create_oval(left[0] - r, left[1] - r, left[0] + r, left[1] + r, fill='yellow')
else:
    canvas.create_oval(right[0] - r, right[1] - r, right[0] + r, right[1] + r, fill='yellow')
if chosen[1]:
    canvas.create_oval(left_goal[0] - r, left_goal[1] - r, left_goal[0] + r, left_goal[1] + r, fill='yellow')
else:
    canvas.create_oval(right_goal[0] - r, right_goal[1] - r, right_goal[0] + r, right_goal[1] + r, fill='yellow')

# ------------------ Predict ------------------
if chosen[0]:
    o1 = left
else:
    o1 = right

if chosen[1]:
    o2 = left_goal
else:
    o2 = right_goal

d0 = as_path.distance(o1, o2)
o1o2 = o2 - o1
o1s = np.array(start) - o1
o2g = np.array(goal) - o2
beta = math.acos(2 * as_path.r / d0)
sm = 2 * math.sqrt((d0 / 2) ** 2 - as_path.r ** 2)

at1 = math.pi - st.dot(o1o2) / math.fabs(st.dot(o1o2)) * (math.pi - math.acos(o1s.dot(o1o2) / (np.linalg.norm(o1s) * np.linalg.norm(o1o2))))
t2b = math.pi - gl.dot(o1o2) / math.fabs(gl.dot(o1o2)) * (math.pi - math.acos(o2g.dot(-o1o2) / (np.linalg.norm(o2g) * np.linalg.norm(-o1o2))))

# ss = (at1 + t2b - 2 * beta) * as_path.r
ss = (at1 + t2b - math.pi) * as_path.r
s = ss + sm
canvas.create_text(width-80, 280, text='Total S:  ' + str(round(s, 3)))



# ------------------- END -----------------
# Draw map
draw_map(size)
for pos_rock in real_topographic:
    create_point(pos_rock, 18, 'gray')

tk.update()
time.sleep(1.5)

# Draw finding path process
for step in as_path.process:
    t += 0.2
    canvas.itemconfigure(timer, text=str(round(t, 2)))
    canvas.itemconfigure(distance, text=str(round(step[2], 3)))

    # save head
    canvas.create_rectangle(step[0][0], step[0][1], step[0][0]+3, step[0][1]+3, fill='brown')
    # save trace
    head, tail = np.array(step[0]), np.array(step[1])
    trace = head + ((head - tail) * 16 / as_path.length).astype(int)  # length

    canvas.create_line(head[0], head[1], trace[0], trace[1], fill='brown', arrow=LAST)
    car = canvas.create_line(step[1][0], step[1][1], step[0][0], step[0][1], fill='black', width=8, arrow=LAST)

    # for i in range(2, len(step)):
    #     create_point(scale_step[i], 10, 'yellow')

    time.sleep(0.5)
    tk.update()

    canvas.delete(car)

# #Draw min path
# for pos in min_path:
#     time.sleep(0.15)
#     create_point(pos, 10, 'red')
#
#     tk.update()

tk.mainloop()
