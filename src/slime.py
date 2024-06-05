import pygame
from settings import *

class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/slime.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 0, slime_width, slime_height, scale=(64, 64))
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.hitbox = self.rect.inflate(-24, -24)

        self.animations = {
            "stand": self.create_animation(self.sprite_sheet, 0, 4, slime_width, slime_height, scale=(64, 64))
        }

        self.animation_speed = ANIMATION_SPEED  
        self.current_frame = 0
        self.current_animation = self.animations["stand"]
        self.last_update_time = pygame.time.get_ticks()

    def get_sprite(self, sheet, x, y, width, height, offset=0, scale=None):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        if scale:
            image = pygame.transform.scale(image, scale)
        return image

    def create_animation(self, sheet, row, num_frames, width, height, scale=None):
        return [self.get_sprite(sheet, i, row, width, height, scale=scale) for i in range(num_frames)]

    def update(self):
        now = pygame.time.get_ticks()
        elapsed_time = (now - self.last_update_time) / 1000.0  

        if elapsed_time > self.animation_speed:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_frame]

        # updejt hitboxów
        self.hitbox.center = self.rect.center
