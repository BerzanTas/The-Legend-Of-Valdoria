from settings import *
import pygame
from time import sleep

class Fireball(pygame.sprite.Sprite):

    def __init__(self, pos, groups, radius, facing, hit_sprites) -> None:
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/fireball.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 0, 48, 48)
        self.rect = self.image.get_rect(topleft=pos)

        self.radius = radius
        self.facing = facing
        self.direction = None
        self.collide = False

        self.shoot_animation = [self.get_sprite(self.sprite_sheet, i, 0, 48, 48) for i in range(4)]
        self.explode_animation = [self.get_sprite(self.sprite_sheet, i, 0, 48, 48, 5*48) for i in range(6)]

        self.image_index = 0
        self.animation_speed = 0.1  # Szybkość animacji pocisku
        self.explosion_speed = 0.1
        self.animation_timer = 0

        self.hit_sprites = hit_sprites

        if self.facing == "up":
            self.rect.move_ip(-15,-15)
            self.direction = "vertical"
            self.vel = FIREBALL_SPEED * -1
            self.image = pygame.transform.rotate(self.image, 90)
            self.shoot_animation = [pygame.transform.rotate(i, 90) for i in self.shoot_animation]
            self.explode_animation = [pygame.transform.rotate(i, 90) for i in self.explode_animation]
        elif self.facing == "down":
            self.rect.move_ip(-15,-10)
            self.direction = "vertical"
            self.vel = FIREBALL_SPEED * 1
            self.image = pygame.transform.rotate(self.image, -90)
            self.shoot_animation = [pygame.transform.rotate(i, -90) for i in self.shoot_animation]
            self.explode_animation = [pygame.transform.rotate(i, -90) for i in self.explode_animation]
        elif self.facing == "left":
            self.rect.move_ip(-40,-20)
            self.direction = "horizontal"
            self.vel = FIREBALL_SPEED * -1
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
            self.shoot_animation = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in self.shoot_animation]
            self.explode_animation = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in self.explode_animation]
        elif self.facing == "right":
            self.rect.move_ip(-10,-20)
            self.direction = "horizontal"
            self.vel = FIREBALL_SPEED * 1
    
    def get_sprite(self, sheet, x, y, width, height, offset = 0):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        return image
    
    def collision(self):
        for sprite in self.hit_sprites:
            if sprite.rect.colliderect(self.rect):
                self.collide = True
                self.image_index = 0
                self.animation_timer = 0
                #self.image = self.get_sprite(self.sprite_sheet, 0, 0, 48, 48, 5*48)

    

    def update(self):
        if not self.collide:
            if self.direction == "vertical":
                self.rect.y += self.vel
            elif self.direction == "horizontal":
                self.rect.x += self.vel
            
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.shoot_animation)
                self.image = self.shoot_animation[self.image_index]

            self.collision()
        else:
            self.animation_timer += self.explosion_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.image_index += 1
                self.image = self.explode_animation[self.image_index]
                
            if self.image_index >= len(self.explode_animation) - 1:
                self.kill()

        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGTH:
            self.kill()
