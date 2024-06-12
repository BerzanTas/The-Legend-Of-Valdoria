import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites, player, level, exp):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.player = player
        self.alive = True
        self.dying = False
        self.font = pygame.font.Font(None, 24)
        self.level_text = self.font.render(f"lvl {level}", True, (255, 255, 255))
        self.exp = exp
    
    def get_sprite(self, sheet, x, y, width, height, offset=0, scale=None, flip=False):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        if scale:
            image = pygame.transform.scale(image, scale)
        if flip:
            image = pygame.transform.flip(image, True, False)
        return image
    
    def create_animation(self, sheet, row, num_frames, width, height, scale=None, flip=False):
        return [self.get_sprite(sheet, i, row, width, height, scale=scale, flip=flip) for i in range(num_frames)]

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        self.image = self.current_animation[self.current_frame]

        if self.is_attacking and self.current_frame == len(self.current_animation) - 1:
            self.is_attacking = False
    
    def update_death_animation(self):
        # Zwolnienie animacji śmierci poprzez użycie `self.animation_speed`
        if self.current_frame < len(self.current_animation) - 1:
            self.current_frame += 1
            self.image = self.current_animation[self.current_frame]
        else:
            self.kill()


    def get_distance_to_player(self):
        enemy_center = pygame.math.Vector2(self.hitbox.center)
        player_center = pygame.math.Vector2(self.player.hitbox.center)
        return enemy_center.distance_to(player_center)
    

    def move_towards_player(self):
        player_pos = pygame.math.Vector2(self.player.hitbox.center)
        enemy_pos = pygame.math.Vector2(self.hitbox.center)
        direction = player_pos - enemy_pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.hitbox.center += direction * self.speed
        self.rect.center = self.rect.center
        self.set_move_animation(direction)

    
    def draw(self, screen, camera):
        camera_pos = self.rect.move(camera.camera.topleft)
        screen.blit(self.image, camera_pos.topleft)
        if self.alive:
            text_rect = self.level_text.get_rect(center=(camera_pos.centerx, camera_pos.top - 10))
            screen.blit(self.level_text, text_rect)
    

    def take_damage(self, amount):
        if self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.dying = True
                self.current_animation = self.animations["death"]
                self.current_frame = 0
                self.player.gain_exp(self.exp)

    def start_attack(self):
        self.set_attack_animation()
        self.is_attacking = True
        self.current_frame = 0

    def check_attack(self, exp):
        if self.hitbox.colliderect(self.player.hitbox):
            now = pygame.time.get_ticks()
            if now - self.last_attack_time > self.attack_cooldown:
                self.player.take_damage(self.attack_damage, exp)
                self.last_attack_time = now


class Skeleton(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites, player, level, exp):
        super().__init__(pos, groups, obstacle_sprites, visible_sprites, player, level, exp)
        
        self.sprite_sheet = pygame.image.load("img/skeleton.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 0, skeleton_width, skeleton_height, scale=(80, 80))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.inflate(-50, -50)

        self.health = 100

        self.speed = skeleton_speed / 300.0  # Prędkość w pikselach na milisekundę
        self.follow_radius = 260  # Radius, w którym skeleton zaczyna śledzić gracza
        self.attack_radius = 30  # Radius ataku
        self.attack_damage = 10
        self.attack_cooldown = 2000  # Czas w milisekundach
        self.last_attack_time = 0

        self.animations = {
                "stand": self.create_animation(self.sprite_sheet, 0, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "death": self.create_animation(self.sprite_sheet, 12, 5, skeleton_width, skeleton_height, scale=(80, 80)),
                "move_top": self.create_animation(self.sprite_sheet, 5, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "move_bottom": self.create_animation(self.sprite_sheet, 3, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "move_right": self.create_animation(self.sprite_sheet, 4, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "move_left": self.create_animation(self.sprite_sheet, 4, 6, skeleton_width, skeleton_height, scale=(80, 80), flip=True),
                "attack_right": self.create_animation(self.sprite_sheet, 7, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "attack_left": self.create_animation(self.sprite_sheet, 7, 6, skeleton_width, skeleton_height, scale=(80, 80), flip=True),
                "attack_down": self.create_animation(self.sprite_sheet, 6, 6, skeleton_width, skeleton_height, scale=(80, 80)),
                "attack_up": self.create_animation(self.sprite_sheet, 8, 6, skeleton_width, skeleton_height, scale=(80, 80))
        }

        self.current_animation = self.animations["stand"]
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.is_attacking = False

        self.animation_speed = 0.2  # Czas w sekundach między klatkami animacji


    def update(self):
        now = pygame.time.get_ticks()
        elapsed_time = (now - self.last_update_time) / 1000.0

        if elapsed_time > self.animation_speed:
            self.last_update_time = now
            if self.alive:
                self.update_animation()
            elif self.dying:
                self.update_death_animation()

        self.rect.centerx = self.hitbox.centerx
        self.rect.centery  = self.hitbox.centery - 15

        if self.alive and not self.dying:
            distance_to_player = self.get_distance_to_player()
            
            if distance_to_player < self.attack_radius:
                if not self.is_attacking:
                    self.start_attack()
                self.check_attack(10)
            elif distance_to_player < self.follow_radius:
                self.move_towards_player()
            else:
                self.current_animation = self.animations["stand"]
                self.is_attacking = False

            # Sprawdzenie granic mapy
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > MAP_WIDTH:
                self.rect.right = MAP_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > MAP_HEIGHT:
                self.rect.bottom = MAP_HEIGHT
            
            
        if not self.alive and self.current_animation == self.animations["death"]:
            self.update_death_animation()


    def set_move_animation(self, direction):
        if abs(direction.y) > abs(direction.x):
            if direction.y < 0:
                self.current_animation = self.animations["move_top"]
            else:
                self.current_animation = self.animations["move_bottom"]
        else:
            if direction.x < 0:
                self.current_animation = self.animations["move_left"]
            else:
                self.current_animation = self.animations["move_right"]

    def set_attack_animation(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        if abs(dx) > abs(dy):
            if dx > 0:
                self.current_animation = self.animations["attack_right"]
            else:
                self.current_animation = self.animations["attack_left"]
        else:
            if dy > 0:
                self.current_animation = self.animations["attack_down"]
            else:
                self.current_animation = self.animations["attack_up"]



class Slime(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites, player, level, exp):
        super().__init__(pos, groups, obstacle_sprites, visible_sprites, player, level, exp)

        self.sprite_sheet = pygame.image.load("img/slime.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 0, slime_width, slime_height, scale=(64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.inflate(-40, -40)
        self.start_pos = pygame.math.Vector2(pos)

        self.health = 50

        self.speed = 1 # movement speed slime'a
        self.attack_radius = 260
        self.attack_damage = 10
        self.attack_cooldown = 1000  # milliseconds
        self.last_attack_time = 0

        self.animations = {
            "stand": self.create_animation(self.sprite_sheet, 0, 4, slime_width, slime_height, scale=(64, 64)),
            "death": self.create_animation(self.sprite_sheet, 12, 5, slime_width, slime_height, scale=(64, 64)),
            "move": self.create_animation(self.sprite_sheet, 6, 7, slime_width, slime_height, scale=(64, 64))
        }

        self.animation_speed = slime_animation
        self.current_frame = 0
        self.current_animation = self.animations["stand"]
        self.last_update_time = pygame.time.get_ticks()
    
    def set_move_animation(self, direction):
        self.current_animation = self.animations["move"]

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
        self.rect.center = self.hitbox.center

        if self.alive and not self.dying:
            self.check_attack(5)

        if not self.alive:
            self.current_animation = self.animations["death"]
        elif self.get_distance_to_player() < self.attack_radius:
            self.move_towards_player()
        else:
            self.current_animation = self.animations["stand"]