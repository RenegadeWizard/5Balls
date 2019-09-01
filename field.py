import pygame
import ball


class Field:
    def __init__(self, position, size, padding, color):
        self.position = position
        self.dimensions = size
        self.padding = padding
        self.color = color
        self.display = pygame.display.get_surface()
        self.ball = None

    def draw(self):
        pygame.draw.rect(self.display, self.color, (self.position[0], self.position[1], self.dimensions, self.dimensions))
        pygame.display.update()
        return self

    def take(self, color):
        self.ball = ball.Ball(self.position, int(self.dimensions/2), color).draw()

    def release(self):
        self.ball = None

    def select(self):
        # self.ball
        pass