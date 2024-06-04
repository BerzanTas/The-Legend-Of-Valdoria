import pygame
from settings import *
from projectile import *

class UI:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.exp_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.spell_font = pygame.font.Font(UI_FONT, 20)

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
        text_surf = self.exp_font.render(str(int(exp)), False, TEXT_COLOR)
        x, y = self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,10), 3)

    def spell_box(self, left, top, spell_img, cooldown, button, time = None):
        bg_rect = pygame.Rect(left, top, SPELL_BOX_SIZE, SPELL_BOX_SIZE)

        if cooldown:
            spell_img = pygame.transform.grayscale(spell_img)
            # renderowanie pozostałego czasu cooldownu
            if time:
                cooldown_time = self.spell_font.render(time, False, TEXT_COLOR)
                cooldown_rect = cooldown_time.get_rect()
                cooldown_rect.topright = (65,5)
                spell_img.blit(cooldown_time, cooldown_rect)
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        spell_rect = spell_img.get_rect(center = bg_rect.center)

        # renderowanie przycisku zaklęcia na obrazie
        button_key = self.spell_font.render(button, False, TEXT_COLOR)
        spell_img.blit(button_key, (5, 5))

        self.display_surface.blit(spell_img, spell_rect)

        


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['mana'], self.mana_bar_rect, MANA_COLOR)

        self.show_exp(player.exp)

        self.spell_box(self.display_surface.get_size()[0]/2 - 110, 630, self.spell_img[0], player.fireball_cooldown, "Space")
        self.spell_box(self.display_surface.get_size()[0]/2 - 35, 630, self.spell_img[1], player.laserbeam_cooldown, "Q", player.get_cooldown_time("laserbeam"))
        #self.spell_box(self.display_surface.get_size()[0]/2 + 40, 630, self.spell_img[1], False, "Q")