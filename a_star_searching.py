import numpy as np
import math


class AStarSearching:
    def __init__(self, size_map, start, goal):
        # value 0, marked = 1, rock = 2, h = 17, start = 5, goal = 9

        self.row, self.column = size_map
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

        self.h_score = np.zeros([self.row, self.column], dtype=float)
        self.g_score = np.full([self.row, self.column], 9999.0)
        self.f_score = np.full([self.row, self.column], 9999.0)


    def distance(self, position1, position2):
        return math.sqrt((position1[0]-position2[0]) ** 2 + (position1[1]-position2[1]) ** 2)


    def calculate_point_line_equation(self, position):
        """
        consider side of point with line
        """
        x, y = position
        vector_sg = self.goal - self.start

        return (y-self.start[1]) / vector_sg[1] - (x-self.start[0]) / vector_sg[0]


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
                        list_wall.append(((i, j-length), length))
                    length = 0

        return list_wall


    def gain(self, mark_map, wall, h_score):
        """
        :return: my coeffection
        """
        pos = wall[0]
        length = wall[1]
        range_gain = 2

        for i in range(-range_gain, range_gain+1):
            if pos[0]+i < 0 or pos[0]+i > self.column:
                return

            for j in range(-range_gain, length + range_gain+1):
                if pos[1]+j < 0 or pos[1]+j > self.row:
                    return
                # if mark_map[pos[0]-i-1][pos[1]+j] == 2:
                #     return
                h_score[pos[0]+i][pos[1]+j] += 5


    def h(self):
        """
        distance euclid
        """
        x, y = self.goal

        # distance euclid
        for i in range(self.row):
            for j in range(self.column):
                self.h_score[i][j] = math.sqrt((i-x) ** 2 + (j-y) ** 2)

        # my coefficient of wall
        # gain with row
        h_score_origin = np.zeros([self.row, self.column], dtype=float)
        mark = self.mark
        print(self.scan_row(mark))

        for wall in self.scan_row(mark):
            self.gain(mark, wall, h_score_origin)

        # gain with column
        h_score_transpose = np.zeros([self.row, self.column], dtype=float)
        mark_transpose = self.mark.transpose()
        print(self.scan_row(mark_transpose))

        for wall in self.scan_row(mark_transpose):
            self.gain(mark_transpose, wall, h_score_transpose)

        self.h_score += h_score_origin + h_score_transpose.transpose()

        return self.h_score


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


    def min_heap(self, queue, i, n):
        left = i * 2
        right = i * 2 + 1
        smallest = i

        # find smallest
        if left < n:
            node_left = queue[left-1]
            if self.f_score[node_left[0]][node_left[1]] < self.f_score[queue[i-1][0]][queue[i-1][1]]:
                smallest = left

        if right < n:
            node_right = queue[left]
            if self.f_score[node_right[0]][node_right[1]] < self.f_score[queue[smallest-1][0]][queue[smallest-1][1]]:
                smallest = right

        # if left < n and self.f_score[node_left[0]][node_left[1]] < self.f_score[queue[i-1][0]][queue[i-1][1]]:
        #     smallest = left
        # else:
        #     smallest = i
        #
        # if right < n and self.f_score[node_right[0]][node_right[1]] < self.f_score[queue[smallest-1][0]][queue[smallest-1][1]]:
        #     smallest = right

        if smallest != i:
            # swap
            queue[i-1], queue[smallest-1] = queue[smallest-1], queue[i-1]

            self.min_heap(queue, smallest, n)


    def insert_queue(self, queue, current):
        queue.append(current)
        pos_current = len(queue)

        f_current = self.f_score[current[0]][current[1]]

        # find parent
        pos_parent = pos_current // 2
        node_parent = queue[pos_parent - 1]

        while pos_current > 1 and self.f_score[node_parent[0]][node_parent[1]] > f_current:
            # swap
            queue[pos_current-1] = node_parent
            queue[pos_parent-1] = current

            pos_current = pos_parent

            # increase pos
            pos_parent = pos_current // 2
            node_parent = queue[pos_parent-1]


    def extract_min_queue(self, queue):
        # get min
        min = queue[0]
        queue[0] = queue[-1]
        queue.pop()

        # rebuild heap
        self.min_heap(queue, 1, len(queue))

        return min


    def a_star(self):
        """
        :return: ~ min path
        """
        open_set = [self.start]  # priority queue

        self.h()
        self.g_score[self.start[0]][self.start[1]] = 0
        self.f_score[self.start[0]][self.start[1]] = 1.25 * self.h_score[self.start[0]][self.start[1]]

        while open_set:
            current = self.extract_min_queue(open_set)
            step = [current]

            if current == self.goal:
                print('\n Distance: ', self.g_score[current[0]][current[1]])
                return self.reconstruct_path(current)

            for neighbor in self.list_neighbor(current):
                tentative_g_score = self.g_score[current[0]][current[1]] + self.distance(current, neighbor)

                if tentative_g_score < self.g_score[neighbor[0]][neighbor[1]]:
                    self.came_from[neighbor[0]][neighbor[1]] = current
                    self.g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                    self.f_score[neighbor[0]][neighbor[1]] = self.g_score[neighbor[0]][neighbor[1]] \
                                                             + 1.25 * self.h_score[neighbor[0]][neighbor[1]]

                if self.mark[neighbor[0]][neighbor[1]] == 0 and (neighbor not in open_set):
                    self.insert_queue(open_set, neighbor)
                    self.mark[neighbor[0]][neighbor[1]] = 1

                    step.append(neighbor)

            self.process.append(step)
        return False
