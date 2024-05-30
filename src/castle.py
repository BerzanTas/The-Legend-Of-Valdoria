import pygame

class Castle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../img/castle.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)