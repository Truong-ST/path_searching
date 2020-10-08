import numpy as np
import math


class AStarSearching:
    def __init__(self, size_map, start, goal):
        # value 0, marked = 1, rock = 2, start = 5, goal = 9

        self.row = size_map[0]
        self.column = size_map[1]
        self.start = start
        self.goal = goal
        self.process = []
        
        self.came_from = []
        for i in range(self.row):
            tmp = []
            for j in range(self.column):
                tmp.append([])
            self.came_from.append(tmp)

        self.mark = np.zeros([self.row, self.column])
        self.mark[start[0]][start[1]] = 1

        self.g_score = np.full([self.row, self.column], 9999.0)
        self.f_score = np.full([self.row, self.column], 9999.0)


    def distance(self, position1, position2):
        return math.sqrt((position1[0]-position2[0]) ** 2 + (position1[1]-position2[1]) ** 2)


    def scan_map(self):
        list_wall = []

        for i in range(len(self.mark)):
            wall = []
            length = 0

            for j in range(len(self.mark[0])):
                if self.mark[i][j] == 2:
                    length += 1
                else:
                    if length > 2:
                        wall.append([[i, j-length], length])
                    length = 0
            if wall:
                list_wall.append(wall)

        return list_wall


    def gain(self, wall, h_score, standard_h):
        pos = wall[0]
        length = wall[1]
        step_exe = length-1

        for i in range(step_exe):
            if pos[0]-1-i < 0:
                return

            for j in range(step_exe-i):
                if self.mark[pos[0]-i-1][pos[1]+j]:
                    return

                h_score[pos[0]-i-1][pos[1]+j] += self.distance(pos, self.goal) * step_exe / standard_h


    def h(self):
        """
        line distance euclid
        """
        h_score = np.zeros([self.row, self.column], dtype=float)
        standard_h = self.distance(self.start, self.goal)
        x, y = self.goal

        for i in range(self.row):
            for j in range(self.column):
                h_score[i][j] = math.sqrt((i-x) ** 2+(j-y) ** 2)

        # my coeffection
        for line in self.scan_map():
            for wall in line:
                self.gain(wall, h_score, standard_h)

        return h_score


    def list_neighbor(self, current):
        """
        :return: list of around(8) current
        """
        list_neighbor = []
        phi = 0

        for i in range(8):
            delta_col = round(math.cos(phi))
            delta_row = round(math.sin(phi))

            next_col = current[1] + delta_col
            next_row = current[0] + delta_row

            if (0 <= next_col < self.column) and (0 <= next_row < self.row):
                list_neighbor.append([next_row, next_col])

            phi += math.pi / 4

        return list_neighbor


    def reconstruct_path(self, current):
        total_path = [current]

        while current != self.start:
            current = self.came_from[current[0]][current[1]]
            total_path.append(current)

        return total_path[:: -1]


    def priority_queue_add(self, queue, current):
        f_current = self.f_score[current[0]][current[1]]

        if queue:
            for i in range(len(queue)):
                if f_current <= self.f_score[queue[i][0]][queue[i][1]]:
                    queue.insert(i, current)
                    return
        queue.append(current)


    def a_star(self):
        """
        :return: ~ min path
        """
        open_set = [self.start]  # heap-min or priority queue
        print(self.scan_map())

        h_score = self.h()
        print(h_score)
        self.g_score[self.start[0]][self.start[1]] = 0
        self.f_score[self.start[0]][self.start[1]] = 1.25 * h_score[self.start[0]][self.start[1]]

        while open_set:
            current = open_set.pop(0)
            step = [current]

            if current == self.goal:
                print('\n done')
                print(self.g_score[current[0]][current[1]])
                return self.reconstruct_path(current)

            for neighbor in self.list_neighbor(current):
                tentative_g_score = self.g_score[current[0]][current[1]] + self.distance(current, neighbor)

                if tentative_g_score < self.g_score[neighbor[0]][neighbor[1]]:
                    self.came_from[neighbor[0]][neighbor[1]] = current
                    self.g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                    self.f_score[neighbor[0]][neighbor[1]] = self.g_score[neighbor[0]][neighbor[1]] \
                                                             + 1.25 * h_score[neighbor[0]][neighbor[1]]

                if self.mark[neighbor[0]][neighbor[1]] == 0 and (neighbor not in open_set):
                    self.priority_queue_add(open_set, neighbor)
                    self.mark[neighbor[0]][neighbor[1]] = 1

                    step.append(neighbor)

            self.process.append(step)
        return False
