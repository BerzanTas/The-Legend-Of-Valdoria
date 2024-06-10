import pygame
from settings import *
from tile import Tile
from player import Player
from slime import Slime
from projectile import Fireball
from ui import UI
from skeleton import Skeleton

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
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.walkable_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()

        # Tworzenie mapy
        self.create_map()

        # UI
        self.ui = UI()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.fireball_sprites, self.visible_sprites)
                elif col == 'x':
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'rock')
                elif col == 'c':
                    castle_pos = (x, y)
                    self.castle = Castle(castle_pos, (self.visible_sprites, self.obstacle_sprites))
                    #self.visible_sprites.change_layer(self.castle, 2)
                elif col == 's':
                    self.slime = Slime((x, y), (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player)
                    #self.visible_sprites.change_layer(self.slime, 1)
                elif col == 'sk':
                    self.slime = Skeleton((x, y), (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player)
                    #self.visible_sprites.change_layer(self.slime, 1)
                elif col == "tr1": #drzewo 1
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'tree1', layer=2)
                elif col == "portal":  # portal
                    Portal((x, y), (self.visible_sprites,))
                elif col == "w":  #woda
                    Water((x, y), (self.visible_sprites, self.obstacle_sprites))
                
    def run(self):

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.fireball_sprites.update()

        self.ui.display(self.player)
    


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, sprite.rect)
    
