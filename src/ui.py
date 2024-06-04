import pygame
from settings import *
from projectile import *

class UI:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(10, 34, MANA_BAR_WIDTH, BAR_HEIGHT)

        self.spell_img = []
        for spell in spell_data.values():
            path = spell['img']
            spell = pygame.image.load(path).convert_alpha()
            self.spell_img.append(spell)

    def show_bar(self, current, max_amount, bg_rect, color):
        # rysowanie tła
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # zmiana statów na piksele
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x, y = self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,10), 3)

    def spell_box(self, left, top, spell_img):
        bg_rect = pygame.Rect(left, top, SPELL_BOX_SIZE, SPELL_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        spell_rect = spell_img.get_rect(center = bg_rect.center)

        self.display_surface.blit(spell_img, spell_rect)


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['mana'], self.mana_bar_rect, MANA_COLOR)

        self.show_exp(player.exp)

        self.spell_box(self.display_surface.get_size()[0]/2 - 85, 650, self.spell_img[0])
        self.spell_box(self.display_surface.get_size()[0]/2 - 25, 650, self.spell_img[0])
        self.spell_box(self.display_surface.get_size()[0]/2 + 35, 650, self.spell_img[0])