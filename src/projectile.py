from settings import *
import pygame

class projectile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, radius, facing) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("img/fireball.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.radius = radius
        self.facing = facing
        self.vel = BALL_SPEED * facing

