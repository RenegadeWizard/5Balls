import pygame
import field
import ball
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
        self.rect_size = int(self.dimensions[0]/self.rect_number * 0.85)
        self.padding = int(self.dimensions[0]/self.rect_number * 0.15)
        self.full_rect = self.rect_size + self.padding
        self.field_list = []

        self.display.fill(dark_gray)      # background
        for i in range(self.rect_number):
            for j in range(self.rect_number):
                self.field_list.append(field.Field((self.padding + i*self.full_rect, self.padding + j*self.full_rect),self.rect_size, self.padding, gray, i*9+j).draw())
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
                mouse_position = pygame.mouse.get_pos()
                toggle_field = self.search_for_field(mouse_position)
                # coloring while dragging
                if toggle_field is not None:
                    toggle_field.select()
                    if toggle_field is not self.colored_field:
                        self.colored_field.unselect()
                        self.colored_field = toggle_field
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
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
                        if selected_field_end.ball is not None:
                            player_choice = 0
                        elif selected_field_end is not None and selected_field_end is not selected_field:
                            print(self.find_path(selected_field, selected_field_end))
                            selected_field_end.ball = selected_field.ball
                            selected_field_end.update_ball()
                            selected_field.ball = None
                            selected_field_end.select()
                            selected_field.draw()
                            selected_field.unselect()
                            selected_field_end.unselect()
                            player_round = False

                if event.type == pygame.QUIT:
                    return True
        return True

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
    def find_path(self, start_field: field.Field, end_field: field.Field):  # TODO: fix it!
        visited = []    # [3,4,5,2,1] -> [vertex]
        adjacent = [start_field.set_score(0, self.distance(start_field.id, end_field.id))]
        path = []

        while adjacent:
            adjacent.sort()
            x = adjacent[0]
            if x.id == end_field.id:
                return path
            adjacent.remove(x)
            visited.append(x)
            print(self.adjacent_list(x.id))
            for y in self.adjacent_list(x.id):
                y = self.field_list[y]
                if y in visited or y.id < 0 or y.id > 80:
                    continue
                tentative_g = self.distance(start_field.id, y.id) + 1  # dunno if ok
                tentative = False
                if y not in adjacent:
                    adjacent.append(y.set_score(self.distance(start_field.id, y.id), self.distance(end_field.id, y.id)))  # nope
                    tentative = True
                elif tentative_g < y.g_score:
                    tentative = True
                if tentative:
                    path.append(y)
        return False

    def f_score(self, id, start, end):
        return self.distance(id, start) + self.distance(id, end)

    def distance(self, start, stop):
        x1 = start % self.rect_number
        x2 = stop % self.rect_number
        y1 = int(start / self.rect_number) - 1  # Think if this is ok
        y2 = int(stop / self.rect_number) - 1
        x = abs(x1 - x2)
        y = abs(y1 - y2)
        return x + y

    def adjacent_list(self, vertex):
        t = [vertex-9, vertex+9]
        if vertex%9:
            t.append(vertex-1)
        elif (vertex-1)%9:
            t.append(vertex+1)
        return t
