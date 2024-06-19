import pygame, sys
from level import Level               
from settings import *
from pyvidplayer import Video
from ui import StartMenu, EndMenu
from player import Player

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.start_menu = StartMenu()
        self.end_menu = EndMenu()
        # changing the title of the window
        pygame.display.set_caption("The Legend of Valdoria")
        self.vid = Video("Intro/Valdoria Intro.mp4")
        self.vid.set_size((WIDTH, HEIGTH))

        pygame.mixer.music.load("sounds/music/valdoria1.mp3")
        for i in range(2,6):
            pygame.mixer.music.queue(f"sounds/music/valdoria{i}.mp3")
    
    def intro(self):
        while self.vid.active:
            self.vid.draw(self.screen, (0,0), False)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.vid.close()
                        self.start()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        self.start()
    
    def start(self):
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            start = self.start_menu.display(events)
            pygame.display.update()

            if start:
                Player.username = self.start_menu.username
                break
        
        self.run()
            

    # main loop
    def run(self):
        
        while True:
            # check the events, and if it is QUIT event then close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

            if Player.dead:
                break
        
        self.end()
            
    
    def end(self):
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            end = self.end_menu.display(events)
            pygame.display.update()

            if end:
                break
        Player.dead = False
        self.start()
                


if __name__ == "__main__":
    game = Game()
    game.intro()