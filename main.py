import pygame, sys
from level import Level
from settings import *

class Game:
    def __init__(self) -> None:
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.level = Level()
        # changing the title of the window
        pygame.display.set_caption("The Legend of Valdoria")

    # main loop
    def run(self):
        while True:
            # check the events, and if it is QUIT event then close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()