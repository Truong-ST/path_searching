import numpy as np
import math
from utilities import *


config_dict = set_configuration('configuration.yaml')
block = config_dict['block']
margin = config_dict['margin']


class AStarSearching:
    def __init__(self, size_map, start, goal, theta_goal, length, v, theta, phi):
        """

        :param size_map: list
        :param start: np.array
        :param goal: coord
        :param length: int
        :param v:
        :param theta:
        :param phi:
        """
        # value 0, marked = 1, rock = 2, h = 17, start = 5, goal = 9

        self.row, self.column = size_map
        self.real_size = [self.row * block, self.column * block]
        self.start, self.goal = start, goal
        self.theta_goal = theta_goal
        self.v = v
        self.length = length
        self.theta = theta
        self.phi = phi
        self.r = self.length / math.tan(self.phi)
        self.total_s = 0

        self.min_phi = math.pi / 8
        self.dt = 1
        self.process = []

        rotate = np.array([[0, 1], [-1, 0]])
        tail_start = self.get_tail(start, self.theta)
        st = np.array(start) - tail_start
        vector_rotate = rotate.dot(st * self.r / self.length)
        center = (st / 2 + tail_start).astype(int)
        self.left_start = np.array(center) + vector_rotate
        self.right_start = np.array(center) - vector_rotate

        tail_goal = self.get_tail(goal, theta_goal)
        gl = np.array(goal) - tail_goal
        vector_rotate_goal = rotate.dot(gl * self.r / self.length)
        center_goal = (gl / 2 + tail_goal).astype(int)

        self.left_goal = np.array(center_goal) + vector_rotate_goal
        self.right_goal = np.array(center_goal) - vector_rotate_goal

        self.came_from = []
        for i in range(self.row):
            tmp = []
            for j in range(self.column):
                tmp.append([])
            self.came_from.append(tmp)

        self.mark = np.zeros([self.row, self.column])
        # pos_start = coord_to_pos(start)
        # self.mark[pos_start[0]][pos_start[1]] = 1

        self.h_score = np.zeros([self.row, self.column], dtype=float)
        # self.g_score = np.full([self.row, self.column], 9999.0)
        # self.f_score = np.full([self.row, self.column], 9999.0)


    def distance(self, position1, position2):
        return np.linalg.norm(position1 - position2)


    def calculate_point_line_equation(self, position):
        """
        consider side of point with line
        """
        x, y = position
        vector_sg = self.goal - self.start

        return (y - self.start[1]) / vector_sg[1] - (x - self.start[0]) / vector_sg[0]


    def scan_row(self, mark):
        """
        find wall
        """
        list_wall = []

        for i in range(len(mark)):
            length = 0
            for j in range(len(mark[0])):
                if mark[i][j] == 2:
                    length += 1
                else:
                    if length > 2:
                        list_wall.append(((i, j - length), length))
                    length = 0

        return list_wall


    def gain(self, mark_map, wall, h_score):
        """
        :return: my coefficient
        """
        pos = wall[0]
        length = wall[1]
        range_gain = 2

        for i in range(-range_gain, range_gain + 1):
            if pos[0] + i < 0 or pos[0] + i > self.column:
                continue

            for j in range(-range_gain, length + range_gain + 1):
                if pos[1] + j < 0 or pos[1] + j > self.row:
                    continue
                if j < 0 or j >= length:
                    h_score[pos[0] + i][pos[1] + j] += (2 - i) * 3 + 60 / (math.sqrt(i ** 2 + j ** 2) + 3)
                else:
                    h_score[pos[0] + i][pos[1] + j] += (2 - i) * 3 + 60 / (i + 3)


    def h(self):
        """
        distance euclid
        """
        x, y = self.goal

        for i in range(self.row):
            for j in range(self.column):
                self.h_score[i][j] = math.sqrt((i - x) ** 2 + (j - y) ** 2)

        # my coefficient of wall

        # gain with row
        # h_score_origin = np.zeros([self.row, self.column], dtype=float)
        # mark = self.mark
        # print("row: ", self.scan_row(mark))
        # for wall in self.scan_row(mark):
        #     self.gain(mark, wall, h_score_origin)
        #
        # # gain with column
        # h_score_transpose = np.zeros([self.row, self.column], dtype=float)
        # mark_transpose = self.mark.transpose()
        # print("column: ", self.scan_row(mark_transpose))
        # for wall in self.scan_row(mark_transpose):
        #     self.gain(mark_transpose, wall, h_score_transpose)
        #
        # self.h_score += h_score_origin + h_score_transpose.transpose()


    def list_neighbor(self, head):
        """
        :return: list of around head
        """
        list_neighbor = []

        max_left_theta = self.theta - self.phi
        max_right_theta = self.theta + self.phi
        max_left = round(max_left_theta / self.min_phi)
        max_right = round(max_right_theta / self.min_phi)

        for i in range(max_left, max_right + 1):
            tmp_theta = i * self.min_phi

            delta_col = round(self.v * math.cos(tmp_theta))
            delta_row = round(self.v * math.sin(tmp_theta))
            # next_col = head[1]+delta_col
            # next_row = head[0]+delta_row
            next_coord = head + np.array([delta_row, delta_col])

            if (0 <= next_coord[1] < self.column * block) and (0 <= next_coord[0] < self.row * block):
                list_neighbor.append(next_coord)

        return list_neighbor


    def reconstruct_path(self, pos_head):
        total_path = [pos_head]
        count = 0
        pos_start = coord_to_pos(self.start)
        while (pos_head[0] != pos_start[0] or pos_head[1] != pos_start[1]) and count < 1000:
            pos_head = self.came_from[pos_head[0]][pos_head[1]]
            total_path.append(pos_head)
            count += 1

        return total_path[:: -1]


    def add_in_max_list(self, lis, head):
        # self.h_score[head[0]][head[1]] += 2
        n = 8

        lis.append(head)
        if len(lis) > n:
            lis.pop(0)


    def choose_circle(self, left_start, left_goal):
        list_choose = [False, False]
        s = np.array(self.start)
        g = np.array(self.goal)
        sg = g - s
        print(sg, left_start, left_goal)

        if sg.dot(left_start) >= 0:
            list_choose[0] = True
        if sg.dot(left_goal) <= 0:
            list_choose[1] = True

        return list_choose


    def get_tail(self, head, theta):
        h0, h1 = head
        t0 = h0 - self.length * math.cos(theta)
        t1 = h1 - self.length * math.sin(theta)
        return np.array([t0, t1]).astype(int)
                        
                        
    def compare_theta(self, theta1, theta2):
        if math.fabs(theta1 % 6.14 - theta2 % 6.14) < self.min_phi:
            return True
        else:
            return False


    def move(self, head, direction):
        x = head[0] + self.v * math.cos(direction)
        y = head[1] + self.v * math.sin(direction)
        return np.array([x, y]).astype(int)


    def find_next(self, head):
        """
        :param head: current
        :return: next head
        """
        max_left = round(-self.phi / self.min_phi)
        max_right = round(self.phi / self.min_phi)

        direction = -1
        d_min = 100000
        min_next = np.array([0, 0])
        pos_head = coord_to_pos(head)
        
        # find phi
        for i in range(max_left, max_right + 1):
            phi = i * self.min_phi
            d_x = self.v * math.cos(self.theta + phi)
            d_y = self.v * math.sin(self.theta + phi)
            next_coord = head + np.array([d_x, d_y]).astype(int)

            if (0 <= next_coord[1] < self.real_size[1]) and (0 <= next_coord[0] < self.real_size[0]):
                pos_next = coord_to_pos(next_coord)

                if self.mark[pos_next[0]][pos_next[1]] == 0:
                    # pos_min = coord_to_pos(min_next)
                    d = self.distance(next_coord, self.goal)
                    print(next_coord, d)

                    if d <= 10:
                        return np.array([-16, 0])
                    if d <= d_min:
                        # self.came_from[pos_next[0]][pos_next[1]] = pos_head
                        d_min = d
                        direction = phi

        next_move = self.move(head, direction+self.theta)
        # self.theta += self.v * math.tan(direction) / self.length
        self.theta += self.v * math.cos(direction) * math.tan(direction) / self.length
        self.total_s += self.v * math.cos(direction)
        print(self.theta, direction)

        return next_move

    
    def a_star(self):
        """
        :return: ~ min path
        """
        # set value
        head = self.start
        pos_goal = coord_to_pos(self.goal)
        self.h()
        self.h_score[0][0] = 999

        count = 0
        while count < 1000:
            tail = self.get_tail(head, self.theta)
            step = [head, tail]

            # pos_head = coord_to_pos(head)
            # if pos_head[0] == pos_goal[0] and pos_head[1] == pos_goal[1]:
            #     # return self.reconstruct_path(pos_head)
            #     return True

            next_head = self.find_next(head)
            if next_head[0] == -16:
                return True

            head = next_head
            step.append(self.total_s)
            self.process.append(step)
            count += 1

        return False
