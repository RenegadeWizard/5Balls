import pygame
import field
import random

# colors (r,g,b)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 0, 255)
cyan = (0, 255, 255)
gray = (200, 200, 200)
dark_gray = (100, 100, 100)
yellow = (255, 255, 0)
orange = (255, 140, 0)

colors = [blue, red, green, white, dark_gray, yellow, orange]


def rand_color():
    return colors[random.randrange(len(colors))]


class Game:
    def __init__(self):
        self.rect_number = 9
        self.display = pygame.display.get_surface()
        self.dimensions = pygame.display.get_window_size()
        self.rect_size = int((self.dimensions[0]-250)/self.rect_number * 0.85)
        self.padding = int((self.dimensions[0]-250)/self.rect_number * 0.15)
        self.full_rect = self.rect_size + self.padding
        self.field_list = []
        self.score = 0

        self.display.fill(dark_gray)      # background
        for i in range(self.rect_number):
            for j in range(self.rect_number):
                self.field_list.append(field.Field((self.padding + i*self.full_rect, self.padding + j*self.full_rect), self.rect_size, self.padding, gray, j*9+i).draw())
        pygame.display.update()
        self.colored_field = self.field_list[0]

    '''
        player's move
    '''
    def play(self):
        player_round = True
        player_choice = 0
        while player_round:
            for event in pygame.event.get():
                position = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # First click
                    if player_choice == 0:
                        selected_field = self.search_for_field(position)
                        if selected_field is not None and selected_field.ball is not None:
                            selected_field.select()
                            player_choice = 1
                        break
                    # Second click
                    elif player_choice == 1:
                        selected_field_end = self.search_for_field(position)
                        if selected_field_end is None or not selected_field.path_to_field:
                            continue
                        if selected_field_end is selected_field:
                            player_choice = 0
                            for i in selected_field.path_to_field:
                                i.unselect()
                            continue
                        if selected_field_end.ball is not None:
                            continue
                        else:
                            for i in self.find_path(selected_field, selected_field_end):
                                i.select()
                            selected_field_end.ball = selected_field.ball
                            selected_field_end.update_ball()
                            selected_field.ball = None
                            selected_field_end.select()
                            selected_field.draw()
                            for i in selected_field.path_to_field:
                                i.unselect()
                            for i in self.strike(selected_field_end):
                                i.ball = None
                                i.draw()
                            player_round = False
                elif player_choice == 1:
                    selecting_field = self.search_for_field(position)
                    if selecting_field is None or selecting_field.ball is not None:
                        continue
                    if selected_field.to_field != selecting_field:
                        if selected_field.path_to_field:
                            selected_field.prev_to_field = selected_field.to_field
                            selected_field.prev_path_to_field = selected_field.path_to_field
                        selected_field.to_field = selecting_field
                        selected_field.path_to_field = self.find_path(selected_field, selecting_field)
                        if selected_field.path_to_field:
                            for i in set(selected_field.prev_path_to_field)-set(selected_field.path_to_field):
                                i.unselect()
                            selected_field.to_field = selecting_field
                            selected_field.path_to_field = self.find_path(selected_field, selecting_field)
                            if not selected_field.path_to_field:
                                continue
                            for i in selected_field.path_to_field:
                                i.select()

                if event.type == pygame.QUIT:
                    return True
                if self.number_of_balls() == 81:
                    return True

        return False

    '''
        creating new balls in between rounds
    '''
    def mid_round(self):
        for i in range(3):
            self.rand_field().take(rand_color())

    '''
        random field that isn't taken
    '''
    def rand_field(self):
        i = random.randrange(len(self.field_list))
        while self.field_list[i].ball is not None:
            i = random.randrange(len(self.field_list))
        return self.field_list[i]

    def search_for_field(self, position):
        for i in self.field_list:
            if position[0] >= i.position[0] and position[1] >= i.position[1] and position[0] <= i.position[0] + i.dimensions and position[1] <= i.position[1] + i.dimensions:
                return i
        return None

    '''
        Implemented A* pathfinding algorithm 
    '''
    def find_path(self, start_field: field.Field, end_field: field.Field):
        visited = []
        adjacent = [start_field]
        came_from = {}
        for i in self.field_list:
            i.set_score(self.distance(end_field.id, i.id), 10000)
        start_field.set_g(0)
        start_field.update_f()

        while adjacent:
            adjacent.sort()
            current = adjacent[0]
            if current.id == end_field.id:
                return self.reconstruct_path(came_from, current)
            adjacent.remove(current)
            visited.append(current)
            for y in self.adjacent_list(current.id):
                y = self.ret_field_from_id(y)
                if y in visited or y.ball is not None:
                    continue
                tentative_g = current.g_score + self.distance(current.id, y.id)
                if tentative_g < y.g_score:
                    came_from[y] = current
                    y.set_g(tentative_g)
                    y.update_f()
                    if y not in adjacent:
                        adjacent.append(y)
        return False

    '''
        Returns field by id
    '''
    def ret_field_from_id(self, field_id):
        for i in self.field_list:
            if i.id == field_id:
                return i
        return False

    '''
        Reconstructs path from A*
    '''
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path

    '''
        distance between two fields
    '''
    def distance(self, start, stop):
        x1 = start % self.rect_number
        x2 = stop % self.rect_number
        y1 = int(start / self.rect_number) - 1
        y2 = int(stop / self.rect_number) - 1
        x = abs(x1 - x2)
        y = abs(y1 - y2)
        return x + y

    '''
        Returns a list of adjacent field ids
    '''
    def adjacent_list(self, vertex):
        t = []
        if vertex - 9 >= 0:
            t.append(vertex-9)
        if vertex + 9 <= 80:
            t.append(vertex+9)
        if vertex % 9:
            t.append(vertex-1)
        if (vertex+1) % 9:
            t.append(vertex+1)
        return t

    def right(self, ball, length, tab):
        temp = self.ret_field_from_id(ball.id + 1)
        if not temp or temp.ball is None or not ((temp.id - 1) % 9) - 8:
            tab.append(ball)
            return length
        if temp.ball.color != ball.ball.color:
            tab.append(ball)
            return length
        else:
            tab.append(ball)
            return self.right(temp, length + 1, tab)

    def left(self, ball, length, tab):
        temp = self.ret_field_from_id(ball.id - 1)
        if not temp or temp.ball is None or not (temp.id % 9) - 8:
            tab.append(ball)
            return length
        if temp.ball.color != ball.ball.color:
            tab.append(ball)
            return length
        else:
            tab.append(ball)
            return self.left(temp, length + 1, tab)

    def top(self, ball, length, tab):
        temp = self.ret_field_from_id(ball.id - 9)
        if not temp or temp.ball is None:
            tab.append(ball)
            return length
        if temp.ball.color != ball.ball.color:
            tab.append(ball)
            return length
        else:
            tab.append(ball)
            return self.top(temp, length + 1, tab)

    def bot(self, ball, length, tab):
        temp = self.ret_field_from_id(ball.id + 9)
        if not temp or temp.ball is None:
            tab.append(ball)
            return length
        if temp.ball.color != ball.ball.color:
            tab.append(ball)
            return length
        else:
            tab.append(ball)
            return self.bot(temp, length + 1, tab)

    def strike(self, ball):
        tab = []
        if self.right(ball, 0, tab) + self.left(ball, 0, tab) >= 4:
            self.score += len(list(set(tab)))
            return list(set(tab))
        tab = []
        if self.top(ball, 0, tab) + self.bot(ball, 0, tab) >= 4:
            self.score += len(list(set(tab)))
            return list(set(tab))
        # if self.five_in_a_row(ball, 0, lt) + self.five_in_a_row(ball, 0, rb) >= 5:
        #     pass
        # if self.five_in_a_row(ball, 0, lb) + self.five_in_a_row(ball, 0, rt) >= 5:
        #     pass
        return []

    def number_of_balls(self):
        sum = 0
        for i in self.field_list:
            sum += 1 if i.ball is not None else 0
        return sum
