import pygame


class Ball:
    def __init__(self, position, radius, color):
        self.radius = int(radius*0.85)
        self.color = color
        self.position = (position[0] + radius, position[1] + radius)
        self.display = pygame.display.get_surface()

    def draw(self):
        pygame.draw.circle(self.display, self.color, self.position, self.radius)
        pygame.display.update()
        return self

    def highlight(self):
        self.color = (self.color[0]+16 > 255 if self.color[0]+16 > 255 else self.color[0], self.color[1]+16 > 255 if self.color[1]+16 > 255 else self.color[1], self.color[2]+16 > 255 if self.color[2]+16 > 255 else self.color[2])