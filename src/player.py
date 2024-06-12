import pygame
from settings import *
from projectile import Fireball, Laserbeam
from enemy import Skeleton, Slime

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, fireball_sprites, visible_sprites):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/playersprite.png").convert_alpha()
        self.image = self.get_sprite(self.sprite_sheet, 0, 11, SPRITE_WIDTH, SPRITE_HEIGHT)  # Pierwsza klatka z 11 rzędu (idle)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-30,-20)

        self.dead = False

        self.obstacle_sprites = obstacle_sprites
        self.fireball_sprites = fireball_sprites
        self.visible_sprites = visible_sprites


        # inicjalizacja kierunku ruchu
        self.direction = pygame.math.Vector2()

        # countdown dla fireball
        self.previous_time_fireball = -2000
        self.fireball_cooldown = False

        # countdown dla laserbeam
        self.previous_time_laserbeam = -30010
        self.laserbeam_cooldown = False

        # EFEKTY GŁOSOWE

        #   efekty chodzenia
        self.footstep_channel = pygame.mixer.Channel(1)
        self.footsteps_sound = pygame.mixer.Sound("sounds/effects/footsteps.mp3")
        self.footsteps_sound.set_volume(0.1)

        # efekt obrażeń
        self.damage_channel = pygame.mixer.Channel(6)
        self.damage_sound = pygame.mixer.Sound("sounds/effects/damage.ogg")
        self.damage_sound.set_volume(0.1)

        # efekt śmierci
        self.death_channel = pygame.mixer.Channel(7)
        self.death_sound = pygame.mixer.Sound("sounds/effects/death.wav")
        self.death_sound.set_volume(0.1)



        # Animacje
        self.animations = {
            "up": self.create_animation(self.sprite_sheet, 8, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "left": self.create_animation(self.sprite_sheet, 9, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "down": self.create_animation(self.sprite_sheet, 10, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "right": self.create_animation(self.sprite_sheet, 11, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "death": self.create_animation(self.sprite_sheet, 20, 6, SPRITE_WIDTH, SPRITE_HEIGHT),
            "attack_up": self.create_attack_animation(47, 8),
            "attack_left": self.create_attack_animation(50, 8),
            "attack_down": self.create_attack_animation(53, 8),
            "attack_right": self.create_attack_animation(56, 8),
        }

        self.current_animation = None
        self.current_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.is_attacking = False

        # Klatki spoczynkowe dla każdego kierunku
        self.idle_frames = {
            "up": self.get_sprite(self.sprite_sheet, 0, 8, SPRITE_WIDTH, SPRITE_HEIGHT),
            "left": self.get_sprite(self.sprite_sheet, 0, 9, SPRITE_WIDTH, SPRITE_HEIGHT),
            "down": self.get_sprite(self.sprite_sheet, 0, 10, SPRITE_WIDTH, SPRITE_HEIGHT),
            "right": self.get_sprite(self.sprite_sheet, 0, 11, SPRITE_WIDTH, SPRITE_HEIGHT)
        }
        self.idle_frame = self.idle_frames["right"]

        # staty
        self.stats = {'health':100, 'mana':70, 'magic':1, 'speed':3}
        self.health = self.stats['health'] * 0.5
        self.mana = self.stats['mana'] * 0.8
        self.exp = 0
        self.level = 1
        self.next_level_exp = 80
        self.speed = self.stats['speed']


        #komunikaty o xp
        self.xp_texts = []

    def get_sprite(self, sheet, x, y, width, height, offset = 0):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        return image

    def create_animation(self, sheet, row, num_frames, width, heigth):
        return [self.get_sprite(sheet, i, row, width, heigth) for i in range(num_frames)]

    def gain_exp(self, amount):
        self.exp += amount
        self.xp_texts.append({'amount': amount, 'timer': pygame.time.get_ticks()})
        if self.exp >= self.next_level_exp:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= self.next_level_exp
        self.next_level_exp = int(self.next_level_exp * 1.5)
    
    def create_attack_animation(self, row, num_frames, width = 64, heigth = 64):
        # Wczytujemy co czwartą klatkę, zaczynając od pierwszej klatki
        return [self.get_sprite(self.sprite_sheet, 3 * i, row, width = width, height = heigth, offset=64) for i in range(num_frames)]

    # Zwraca liczbę sekund które pozostały do ponownego użycia zaklęcia
    def get_cooldown_time(self, spell) -> str:
        if spell == "laserbeam":
            miliseconds = spell_data['laserbeam']['cooldown'] - (self.current_time - self.previous_time_laserbeam)
            seconds = int(miliseconds/1000)

        return str(seconds)
    
    def take_damage(self, amount):
        if not self.dead:
            if self.health <= 0:
                self.sound_player("death")
                self.health = 0
                self.dead = True
                self.current_frame = 0
            else:
                self.sound_player("damage")
                self.health -= amount

        print(f"Player health: {self.health}")
        print(self.dead)
    
    def sound_player(self, sound_type):
        if sound_type == "footsteps" and not self.footstep_channel.get_busy():
            self.footstep_channel.play(self.footsteps_sound)
        elif sound_type == "damage" and not self.damage_channel.get_busy():
            self.damage_channel.play(self.damage_sound)
        elif sound_type == "death" and not self.death_channel.get_busy():
            self.death_channel.play(self.death_sound)


    def update(self):

        if self.dead:
            self.current_animation = self.animations["death"]
            if self.current_frame >= len(self.current_animation) - 1:
                self.kill()
        else:
            self.current_time = pygame.time.get_ticks()
            self.fireball_cooldown = False if self.current_time - self.previous_time_fireball >= spell_data['fireball']['cooldown'] else True
            self.laserbeam_cooldown = False if self.current_time - self.previous_time_laserbeam >= spell_data["laserbeam"]["cooldown"]  else True
        
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
                    if not self.fireball_cooldown:
                        self.is_attacking = True
                        if self.idle_frame == self.idle_frames["up"]:
                            self.current_animation = self.animations["attack_up"]
                            self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "up", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["left"]:
                            self.current_animation = self.animations["attack_left"]
                            self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "left", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["down"]:
                            self.current_animation = self.animations["attack_down"]
                            self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "down", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["right"]:
                            self.current_animation = self.animations["attack_right"]
                            self.projectile = Fireball(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "right", hit_sprites=self.obstacle_sprites)

                        self.previous_time_fireball = self.current_time
                    

                elif keys[pygame.K_q]:
                    if not self.laserbeam_cooldown:
                        self.is_attacking = True
                        if self.idle_frame == self.idle_frames["up"]:
                            self.current_animation = self.animations["attack_up"]
                            self.projectile = Laserbeam(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "up", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["left"]:
                            self.current_animation = self.animations["attack_left"]
                            self.projectile = Laserbeam(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "left", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["down"]:
                            self.current_animation = self.animations["attack_down"]
                            self.projectile = Laserbeam(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "down", hit_sprites=self.obstacle_sprites)
                        elif self.idle_frame == self.idle_frames["right"]:
                            self.current_animation = self.animations["attack_right"]
                            self.projectile = Laserbeam(self.rect.center, (self.visible_sprites, self.fireball_sprites), facing = "right", hit_sprites=self.obstacle_sprites)

                        self.previous_time_laserbeam = self.current_time
            
            else:
                if self.current_frame >= len(self.current_animation) - 1:
                    self.is_attacking = False
                    self.current_frame = 0

        # efekt głosowy chodzenia
        if self.direction.x != 0 or self.direction.y != 0:
            self.sound_player("footsteps")
        else:
            self.footstep_channel.stop()

        self.move(self.speed)

        # Sprawdzenie granic mapy
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > MAP_WIDTH:
            self.hitbox.right = MAP_WIDTH
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        if self.hitbox.bottom > MAP_HEIGHT:
            self.hitbox.bottom = MAP_HEIGHT



        # Aktualizacja ramki animacji
        if self.current_animation:
            speed = ATTACK_ANIMATION_SPEED if self.is_attacking else ANIMATION_SPEED
            self.current_frame = (self.current_frame + speed) % len(self.current_animation)
            self.image = self.current_animation[int(self.current_frame)]
        else:
            self.image = self.idle_frame  # Postać w spoczynku
        
        self.update_xp_texts()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Aktualizacja pozycji gracza
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery-10


    def collision(self, direction):
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if isinstance(sprite, Slime):
                        continue  # ignoruj kolizję z slime
                    if isinstance(sprite, Skeleton):
                        continue
            
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


    ########## odnośnie lvl ############
    def update_xp_texts(self):
        current_time = pygame.time.get_ticks()
        self.xp_texts = [text for text in self.xp_texts if current_time - text['timer'] <= 1000]
