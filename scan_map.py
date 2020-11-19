import numpy as np
import math
import time
from tkinter import *
from utilities import *


config_dict = set_configuration('configuration.yaml')
width = config_dict['width']
width += -100
height = config_dict['height']
block = config_dict['block']
margin = config_dict['margin']


def build_border(map, size):
    for row in range(size[0]):
        for col in range(size[1]):
            if row == 0 or row == size[0] - 1 or col == 0 or col == size[1] - 1:
                map[row][col] = 2


def create_point(position, size, color):
    canvas.create_rectangle(position[0], position[1], position[0]+size, position[1]+size, fill=color)


class Scanner:
    def __init__(self, file_map, size):
        self.file_map = file_map
        self.size = size
        self.risk_map = np.zeros(size)

        self.origin_map = np.zeros(size)
        mark = get_topographic('map.csv')
        for pos in mark:
            self.origin_map[pos[1]][pos[0]] = 2
        build_border(self.origin_map, size)

        self.list_barrie = []
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.origin_map[row][col] == 2:
                    self.list_barrie.append([row, col])


    def draw_map(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.origin_map[row][col] == 2:
                    canvas.create_rectangle(col * block + margin, row * block + margin, col * block + margin + block - 2,
                                            row * block + margin + block - 2, fill='gray')
                else:
                    canvas.create_rectangle(col * block + margin, row * block + margin, col * block + margin + 1,
                                            row * block + margin + 1, fill='black')


    def normal_evaluate(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.origin_map[row][col] == 2:
                    continue

                risk = 0
                scope = 2
                # for pos in self.list_barrie:
                #     risk += math.sqrt((row - pos[0]) ** 2 + (col - pos[1]) ** 2)
                for i in range(row-scope, row+1+scope):
                    for j in range(col-scope, col+1+scope):
                        if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
                            if self.origin_map[i][j] == 2 and (i != row or j != col):
                                risk += 48 / ((i - row) ** 4 + (j - col) ** 4)

                self.risk_map[row][col] = risk


    def show_risk_map(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.origin_map[row][col] == 2:
                    canvas.create_rectangle(col * block + margin, row * block + margin,
                                            col * block + margin + block - 2,
                                            row * block + margin + block - 2, fill='gray')
                    continue
                canvas.create_text(col * block + margin + 8, row * block + margin + 8, text=str(int(self.risk_map[row][col])))


    def visualize_risk_map(self):
        thresh_low = 7
        thresh_high = 22
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.origin_map[row][col] == 2:
                    canvas.create_rectangle(col * block + margin, row * block + margin,
                                            col * block + margin + block - 2,
                                            row * block + margin + block - 2, fill='black')
                    continue
                if self.risk_map[row][col] < thresh_low:
                    create_point((col * block + margin, row * block + margin), block - 2, 'green2')
                elif thresh_low <= self.risk_map[row][col] < thresh_high:
                    create_point((col * block + margin, row * block + margin), block - 2, 'yellow')
                else:
                    create_point((col * block + margin, row * block + margin), block - 2, 'orangered')


    def mini_car(self, start):
        pass





if __name__ == '__main__':
    tk = Tk()
    tk.title('risk map - color')
    canvas = Canvas(tk, width=width, height=height)
    tk.resizable(0, 0)
    canvas.pack()

    size = [35, 35]
    scanner = Scanner('map.csv', size)
    scanner.normal_evaluate()
    # build_border(scanner.origin_map, size)
    scanner.visualize_risk_map()

    root = Tk()
    root.title('risk map - number')
    canvas = Canvas(root, width=width, height=height)
    tk.resizable(0, 0)
    canvas.pack()

    scanner.show_risk_map()


    root.mainloop()
    tk.mainloop()
