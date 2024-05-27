import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../img/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pygame.Surface((64,64)) #size
        self.image.fill('yellow') #color
        