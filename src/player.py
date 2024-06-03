import pygame
from settings import *
from projectile import Fireball

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, fireball_sprites, visible_sprites):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/playersprite.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 11, SPRITE_WIDTH, SPRITE_HEIGHT)  # Pierwsza klatka z 11 rzędu (idle)
        self.obstacle_sprites = obstacle_sprites
        self.fireball_sprites = fireball_sprites
        self.visible_sprites = visible_sprites

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.hitbox = self.rect.inflate(-5,-5)

        #Inicjalizacja kierunku ruchu
        self.direction = pygame.math.Vector2(0, 0)

        #countdown dla fireball
        self.previous_time = pygame.time.get_ticks()


        # Animacje
        self.animations = {
            "up": self.create_animation(self.sprite_sheet, 8, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "left": self.create_animation(self.sprite_sheet, 9, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "down": self.create_animation(self.sprite_sheet, 10, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "right": self.create_animation(self.sprite_sheet, 11, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "attack_up": self.create_attack_animation(47, 8),
            "attack_left": self.create_attack_animation(50, 8),
            "attack_down": self.create_attack_animation(53, 8),
            "attack_right": self.create_attack_animation(56, 8),
        }

        self.current_animation = None
        self.current_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.is_attacking = False

        # Prędkość poruszania się
        self.speed = PLAYER_SPEED

        # Klatki spoczynkowe dla każdego kierunku
        self.idle_frames = {
            "up": self.get_sprite(self.sprite_sheet, 0, 8, SPRITE_WIDTH, SPRITE_HEIGHT),
            "left": self.get_sprite(self.sprite_sheet, 0, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "down": self.get_sprite(self.sprite_sheet, 0, 10, SPRITE_WIDTH, SPRITE_HEIGHT),
            "right": self.get_sprite(self.sprite_sheet, 0, 11, SPRITE_WIDTH, SPRITE_HEIGHT)
        }
        self.idle_frame = self.idle_frames["right"]

    def get_sprite(self, sheet, x, y, width, height, offset = 0):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        return image

    def create_animation(self, sheet, row, num_frames, width, heigth):
        return [self.get_sprite(sheet, i, row, width, heigth) for i in range(num_frames)]

    def create_attack_animation(self, row, num_frames, width = 64, heigth = 64):
        # Wczytujemy co czwartą klatkę, zaczynając od pierwszej klatki
        return [self.get_sprite(self.sprite_sheet, 3 * i, row, width = width, height = heigth, offset=64) for i in range(num_frames)]

    def update(self):

        keys = pygame.key.get_pressed()
        if not self.is_attacking:
            self.current_animation = None
            self.direction.x = 0
            self.direction.y = 0

            if keys[pygame.K_UP]:
                self.current_animation = self.animations["up"]
                self.direction.y = -1
                self.idle_frame = self.idle_frames["up"]
            elif keys[pygame.K_LEFT]:
                self.current_animation = self.animations["left"]
                self.direction.x = -1
                self.idle_frame = self.idle_frames["left"]
            elif keys[pygame.K_DOWN]:
                self.current_animation = self.animations["down"]
                self.direction.y = 1
                self.idle_frame = self.idle_frames["down"]
            elif keys[pygame.K_RIGHT]:
                self.current_animation = self.animations["right"]
                self.direction.x = 1
                self.idle_frame = self.idle_frames["right"]
            elif keys[pygame.K_SPACE]:
                self.current_time = pygame.time.get_ticks()
                self.can_shoot = True if self.current_time - self.previous_time > 1000 else False
                
                if self.can_shoot:
                    self.is_attacking = True
                    if self.idle_frame == self.idle_frames["up"]:
                        self.current_animation = self.animations["attack_up"]
                        self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), radius=5, facing = "up", hit_sprites=self.obstacle_sprites)
                    elif self.idle_frame == self.idle_frames["left"]:
                        self.current_animation = self.animations["attack_left"]
                        self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), radius=5, facing = "left", hit_sprites=self.obstacle_sprites)
                    elif self.idle_frame == self.idle_frames["down"]:
                        self.current_animation = self.animations["attack_down"]
                        self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), radius=5, facing = "down", hit_sprites=self.obstacle_sprites)
                    elif self.idle_frame == self.idle_frames["right"]:
                        self.current_animation = self.animations["attack_right"]
                        self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), radius=5, facing = "right", hit_sprites=self.obstacle_sprites)
                    
                    self.previous_time = self.current_time
                
        else:
            if self.current_frame >= len(self.current_animation) - 1:
                self.is_attacking = False
                self.current_frame = 0

        # Aktualizacja pozycji gracza
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


        # Sprawdzenie granic mapy
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > MAP_HEIGHT:
            self.rect.bottom = MAP_HEIGHT



        # Aktualizacja ramki animacji
        if self.current_animation:
            speed = ATTACK_ANIMATION_SPEED if self.is_attacking else ANIMATION_SPEED
            self.current_frame = (self.current_frame + speed) % len(self.current_animation)
            self.image = self.current_animation[int(self.current_frame)]
        else:
            self.image = self.idle_frame  # Postać w spoczynku


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
