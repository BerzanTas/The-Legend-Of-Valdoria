import pygame
from settings import *

class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites, player):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/slime.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 0, slime_width, slime_height, scale=(64, 64))
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.player = player

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.start_pos = pygame.math.Vector2(pos)  # pozycja startowa slime'a

        self.font = pygame.font.Font(None, 24)
        self.level_text = self.font.render("lvl 1", True, (255, 255, 255))

        self.hitbox = self.rect.inflate(-40, -40)

        self.health = 50  # życie slime
        self.alive = True
        self.dying = False

        self.speed = 2 # movement speed slime'a
        self.attack_radius = 150
        self.attack_damage = 10
        self.attack_cooldown = 1000  # milliseconds
        self.last_attack_time = 0

        self.animations = {
            "stand": self.create_animation(self.sprite_sheet, 0, 4, slime_width, slime_height, scale=(64, 64)),
            "death": self.create_animation(self.sprite_sheet, 12, 5, slime_width, slime_height, scale=(64, 64)),
            "move": self.create_animation(self.sprite_sheet, 6, 7, slime_width, slime_height, scale=(64, 64))
        }

        self.animation_speed = slime_aniamtion
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
            if not self.dying:
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
                self.image = self.current_animation[self.current_frame]
            elif self.dying:
                if self.current_frame < len(self.current_animation) - 1:
                    self.current_frame += 1
                    self.image = self.current_animation[self.current_frame]
                else:
                    self.kill()  # usuwanie slime z mapy

        # upodejtowanie pozycji hitboxu
        self.hitbox.center = self.rect.center

        if self.alive and not self.dying:
            self.check_attack()

        if not self.alive:
            self.current_animation = self.animations["death"]
        elif self.within_attack_radius():
            self.move_towards_player()
        else:
            self.current_animation = self.animations["stand"]

    def within_attack_radius(self):
        slime_center = pygame.math.Vector2(self.rect.center)
        player_center = pygame.math.Vector2(self.player.rect.center)
        distance = slime_center.distance_to(player_center)
        return distance < self.attack_radius

    def check_attack(self):
        # sprawdzanie kolizji do ataku
        if self.hitbox.colliderect(self.player.hitbox):
            now = pygame.time.get_ticks()
            if now - self.last_attack_time > self.attack_cooldown:
                self.player.take_damage(self.attack_damage)
                self.last_attack_time = now

    def move_towards_player(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        slime_pos = pygame.math.Vector2(self.rect.center)
        direction = player_pos - slime_pos
        if direction.length() != 0:
            direction = direction.normalize()
            self.rect.center += direction * self.speed
            self.hitbox.center = self.rect.center  # aktualizacja hitboxu
            self.current_animation = self.animations["move"]

    def take_damage(self, amount):
        if self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.dying = True
                self.current_animation = self.animations["death"]
                self.current_frame = 0

    def draw(self, screen, camera):
        camera_pos = self.rect.move(camera.camera.topleft)
        screen.blit(self.image, camera_pos.topleft)
        if self.alive:
            text_rect = self.level_text.get_rect(center=(camera_pos.centerx, camera_pos.top - 10))
            screen.blit(self.level_text, text_rect)
