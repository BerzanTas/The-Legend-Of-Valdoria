import pygame
from settings import *
from tile import Tile
from player import Player
from projectile import Fireball
from ui import UI
from enemy import Skeleton, Slime, Nightborne, Enemy
from elements import *

class Level:
    def __init__(self):
        # Pobierz powierzchnię wyświetlania
        self.display_surface = pygame.display.get_surface()

        self.grass_image = pygame.image.load("img/assets/grass.png").convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE,TILESIZE))

        # Grupy sprite'ów (dodanie warstwowania)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.walkable_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        self.decor_sprites = pygame.sprite.Group()

        # Tworzenie mapy
        self.create_map()

        # UI
        self.ui = UI()

        #lista obiektów do respawnu
        self.respawn_list = []

    # funkcja która tworzy mapę w oparciu o listę znajdującą się w module settings.py
    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.fireball_sprites, self.visible_sprites)
        
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'rock')
                elif col == 's':
                    self.slime = Slime((x, y), (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player, 1, exp=50, level_instance=self)
                elif col == 'sk':
                    self.slime = Skeleton((x, y), (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player, 3, exp=150, level_instance=self)
                elif col == "tr1": #drzewo 1
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'tree1', layer=2)
                elif col == "portal":  # portal
                    Portal((x, y), (self.visible_sprites,))
                elif col == "w":  #woda
                    Water((x, y), (self.visible_sprites, self.obstacle_sprites))
                elif col == "tr2":
                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'tree2', layer=2)
                elif col == "dc":
                    Tile((x,y), (self.visible_sprites, self.decor_sprites), 'decor', layer=2)
                elif col == "kr":
                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'krzew', layer=2)
                elif col == "tb":
                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'tablica', layer=2)
                elif col == "hd":
                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'head', layer=2)
                elif col == "borne":
                    self.night = Nightborne((x, y), (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player, 50, 500, level_instance=self)
                elif col == "bld":  #woda
                    bloodtower((x, y), (self.visible_sprites, self.obstacle_sprites))

    def draw_background(self):
        for row in range(0, MAP_HEIGHT, TILESIZE):
            for col in range(0, MAP_WIDTH, TILESIZE):
                self.display_surface.blit(self.grass_image, (col, row))
                
    def run(self):
        self.draw_background()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.fireball_sprites.update()

        self.ui.display(self.player)

        #aktualizacja respawnu
        self.update_respawn()
        
    def update_respawn(self):
        current_time = pygame.time.get_ticks()
        for respawn_info in self.respawn_list[:]:
            if current_time - respawn_info['death_time'] > 6000:  # 1 minuta = 60000 ms
                enemy_class = respawn_info['class']
                pos = respawn_info['pos']
                level = respawn_info['level']
                exp = respawn_info['exp']
                new_enemy = enemy_class(pos, (self.visible_sprites, self.obstacle_sprites), self.obstacle_sprites, self.visible_sprites, self.player, level, exp, level_instance=self)
                self.respawn_list.remove(respawn_info)

    def add_to_respawn_list(self, enemy):
        respawn_info = {
            'class': enemy.__class__,
            'pos': enemy.rect.topleft,
            'level': enemy.level,
            'exp': enemy.exp,
            'death_time': pygame.time.get_ticks()
        }
        self.respawn_list.append(respawn_info)
    
class YSortCameraGroup(pygame.sprite.Group):
    """Klasa odpowiedzialna za kamerę oraz przemieszczania elementów względem kamery"""

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.grass_image = pygame.image.load("img/assets/grass.png").convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE, TILESIZE))

        self.user_font = pygame.font.Font(SPELL_FONT, 14)

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.offset.x = max(0, min(self.offset.x, MAP_WIDTH - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, MAP_HEIGHT - self.display_surface.get_height()))

        # rozdzielamy decor sprites i nondecor sprites
        decor_sprites = [sprite for sprite in self.sprites() if getattr(sprite, 'is_decor', False)]
        non_decor_sprites = [sprite for sprite in self.sprites() if not getattr(sprite, 'is_decor', False)]

        # najpierw rysujemy elementy decor
        for sprite in sorted(decor_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # rysujemy resztę elementów
        for sprite in sorted(non_decor_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            if isinstance(sprite, Enemy):
                sprite.draw_name(self.display_surface, self.offset)

        # Rysowanie gracza
        self.display_surface.blit(player.image, player.rect.topleft - self.offset)

        # Rysowanie XP i poziomu gracza
        self.draw_xp_texts(player)
        self.show_username(player.username, player)
        self.show_level(player)

    def draw_xp_texts(self, player):
        for text in player.xp_texts:
            xp_surface = pygame.font.Font(None, 20).render(f"+{text['amount']}xp", True, (255, 255, 0))
            offset_pos = pygame.Vector2(player.rect.centerx, player.rect.top + 30) - self.offset
            self.display_surface.blit(xp_surface, offset_pos)
    
    def show_username(self, username, player):
        username_surf = self.user_font.render(username, False, TEXT_COLOR)
        offset_pos = pygame.Vector2(player.rect.centerx - username_surf.get_width() // 2, player.rect.top - 20) - self.offset
        self.display_surface.blit(username_surf, offset_pos)
    
    def show_level(self,player):
        level_surf = self.user_font.render(f"lvl {player.level}", False, TEXT_COLOR)
        offset_pos = pygame.Vector2(player.rect.centerx - level_surf.get_width() // 2, player.rect.top - 5) - self.offset
        self.display_surface.blit(level_surf, offset_pos)