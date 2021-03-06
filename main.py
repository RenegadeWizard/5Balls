import pygame
import menu
import game


def main():
    pygame.init()
    pygame.display.set_caption("5Balls")
    display = pygame.display.set_mode((1000, 750), 0)
    points = menu.Menu()

    game_on = True
    game_console = game.Game()
    points.render()
    '''
        Main game loop
    '''
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                break
        game_console.mid_round()
        if game_console.play():
            break
        pygame.display.update()
        points.score(game_console.score)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
