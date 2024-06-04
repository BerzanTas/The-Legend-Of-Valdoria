import pygame
from settings import *
from tile import Tile
from player import Player
from castle import Castle
from projectile import Fireball
from ui import UI

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGTH / 2)

        # Limit scroll to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - WIDTH), x)  # Right
        y = max(-(self.height - HEIGTH), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

class Level:
    def __init__(self):
        # Pobierz powierzchnię wyświetlania
        self.display_surface = pygame.display.get_surface()

        self.grass_image = pygame.image.load("img/grass.png").convert_alpha()
        # Grupy sprite'ów (dodanie warstwowania)
        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.obstacle_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()

        # Tworzenie mapy
        self.create_map()

        self.camera = Camera(len(WORLD_MAP[0]) * TILESIZE, len(WORLD_MAP) * TILESIZE)

        # UI
        self.ui = UI()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'rock')
                elif col == 'p':
                    self.player = Player((x, y), (self.visible_sprites,), self.obstacle_sprites, self.fireball_sprites, self.visible_sprites)
                    print(self.player.rect)
                    self.visible_sprites.change_layer(self.player, 1)
                elif col == 'c':
                    castle_pos = (x, y)
                    self.castle = Castle(castle_pos, (self.visible_sprites, self.obstacle_sprites))
                    self.visible_sprites.change_layer(self.castle, 2)


    def run(self):
        for x in range(0, WIDTH, self.grass_image.get_width()):
            for y in range(0, HEIGTH, self.grass_image.get_height()):
                self.display_surface.blit(self.grass_image, (x, y))
                
        self.visible_sprites.update()
        self.camera.update(self.player)
        self.fireball_sprites.update()

        self.ui.display(self.player)

        # Rysowanie sprite'ów z przesunięciem kamery
        for sprite in self.visible_sprites:
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))
