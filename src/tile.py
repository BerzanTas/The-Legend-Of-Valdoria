import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type):
        super().__init__(groups)
        if tile_type == 'rock':
            self.image = pygame.image.load("../img/rock.png").convert_alpha()
        elif tile_type == 'fences':
            self.image = pygame.image.load("../img/fences.png").convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        # Przypisz kafelki do niższej warstwy
        for group in groups:
            if isinstance(group, pygame.sprite.LayeredUpdates):
                group.add(self, layer=0)


        