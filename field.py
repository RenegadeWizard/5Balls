import pygame
import ball


class Field:
    def __init__(self, position, size, padding, color, field_id):
        self.position = position
        self.dimensions = size
        self.padding = padding
        self.color = color
        self.display = pygame.display.get_surface()
        self.ball = None
        self.id = field_id
        self.g_score = None
        self.h_score = None
        self.f_score = None

    def __lt__(self, other):
        return self.f_score < other.f_score

    def set_score(self, h, g):
        self.h_score = h
        self.g_score = g
        self.f_score = h + g
        return self

    def draw(self):
        pygame.draw.rect(self.display, self.color, (self.position[0], self.position[1], self.dimensions, self.dimensions))
        pygame.display.update()
        return self

    def take(self, color):
        self.ball = ball.Ball(self.position, int(self.dimensions/2), color).draw()

    def release(self):
        self.ball = None

    def select(self):
        self.highlight()

    def unselect(self):
        self.color = (200, 200, 200)
        self.draw()
        if self.ball is not None:
            self.ball.draw()

    def highlight(self):
        self.color = (150, 150, 150)
        self.draw()
        if self.ball is not None:
            self.ball.draw()

    def update_ball(self):
        self.ball.position = (self.position[0] + int(self.dimensions/2), self.position[1] + int(self.dimensions/2))
