import pygame


class Menu:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Arial", 52)
        self.label = self.font.render("Points: ", 1, (255, 255, 255))
        self.points = self.font.render("0", 1, (255, 255, 255))
        # pygame.draw.rect(self.display, (255, 255, 255), (850, 300, 150, 300)) # TODO: Reset button

    def render(self):
        self.display.blit(self.label, (790, 100))
        self.display.blit(self.points, (850, 175))

    def score(self, point):
        self.points = self.font.render(str(point), 1, (255, 255, 255))
        pygame.draw.rect(self.display, (100, 100, 100), (850, 175, 60, 60))
        pygame.display.update((850, 175, 60, 60))
        self.display.blit(self.points, (850, 175))
