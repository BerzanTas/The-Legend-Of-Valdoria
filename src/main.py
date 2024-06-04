import pygame, sys
from level import Level               
from settings import *
from pyvidplayer import Video

class Game:                
    def __init__(self) -> None:
        # setupq
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.level = Level()
        # changing the title of the window
        pygame.display.set_caption("The Legend of Valdoria")
        self.vid = Video("Intro/Valdoria Intro.mp4")
        self.vid.set_size((WIDTH, HEIGTH))
    
    def intro(self):
        while self.vid.active:
            self.vid.draw(self.screen, (0,0), False)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.vid.close()
                        self.run()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        self.run()

    # main loop
    def run(self):
        while True:
            # check the events, and if it is QUIT event then close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('green')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.intro()