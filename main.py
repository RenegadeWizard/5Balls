import pygame
import menu
import game


def main():
    pygame.init()
    pygame.display.set_caption("5 kulek")
    display = pygame.display.set_mode((750, 750), 0)

    game_on = True
    game_console = game.Game()

    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                break
        game_console.mid_round()
        game_console.play()
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()