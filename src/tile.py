import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type, layer=0):
        super().__init__(groups)
        if tile_type == 'rock':
            self.image = pygame.image.load("img/rock.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40,40))
        elif tile_type == 'tree1':
            self.image = pygame.image.load("img/tree1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (70,80))

        self.rect = self.image.get_rect(topleft=pos)
        self.rect = self.rect.inflate(-10, -10) 
        self.hitbox = self.rect.inflate(-20,-20)

        # Przypisz kafelki do określonej warstwy
        for group in groups:
            if isinstance(group, pygame.sprite.LayeredUpdates):
                group.add(self, layer=layer)

        