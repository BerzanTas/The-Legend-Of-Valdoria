import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type, layer=0):
        super().__init__(groups)
        if tile_type == 'rock':
            self.image = pygame.image.load("img/rock.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (24,24))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-5)
        elif tile_type == 'tree1':
            self.image = pygame.image.load("img/tree1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (70,80))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-40,-40)
        elif tile_type == 'tree2':
            self.image = pygame.image.load("img/tree2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32,16))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-20)
        elif tile_type == 'decor':
            self.image = pygame.image.load("img/decor.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (64,64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-5)
        elif tile_type == 'krzew':
            self.image = pygame.image.load("img/krzew.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32,32))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-5)
        elif tile_type == 'tablica':
            self.image = pygame.image.load("img/tablica.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (32,32))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-5)
        elif tile_type == 'head':
            self.image = pygame.image.load("img/head.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (24,24))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5,-5)

        

        

        # Przypisz kafelki do określonej warstwy
        for group in groups:
            if isinstance(group, pygame.sprite.LayeredUpdates):
                group.add(self, layer=layer)

        