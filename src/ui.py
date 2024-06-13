import pygame
from settings import *
from projectile import *

class UI:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.exp_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.spell_font = pygame.font.Font(SPELL_FONT, 20)
        self.cooldown_font = pygame.font.FontType(UI_FONT, 28)

        # bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(10, 34, MANA_BAR_WIDTH, BAR_HEIGHT)

        self.spell_img = []
        for spell in spell_data.values():
            path = spell['img']
            spell = pygame.image.load(path).convert_alpha()
            spell = pygame.transform.scale(spell, (64,64))
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

    def spell_box(self, left, top, spell_img, cooldown, button, mana_cost, time = None):
        bg_rect = pygame.Rect(left, top, SPELL_BOX_SIZE, SPELL_BOX_SIZE)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        spell_rect = spell_img.get_rect(center = bg_rect.center)

        # renderowanie przycisku zaklęcia na obrazie
        button_key = self.spell_font.render(button, False, 'white')
        
        mana_cost = self.spell_font.render(str(mana_cost), False, "white")
        mana_cost_rect = mana_cost.get_rect()
        mana_cost_rect.bottomright = spell_img.get_rect().bottomright

        if cooldown:
            spell_img = pygame.transform.grayscale(spell_img)
            # renderowanie pozostałego czasu cooldownu
            if time:
                cooldown_time = self.cooldown_font.render(time, False, COOLDOWN_COLOR)
                cooldown_rect = cooldown_time.get_rect()
                cooldown_rect.center = spell_img.get_rect().center
                spell_img.blit(cooldown_time, cooldown_rect)

                button_key.set_colorkey('red')
        
        self.display_surface.blit(spell_img, spell_rect)
        spell_img.blit(button_key, (5, 0))
        spell_img.blit(mana_cost, mana_cost_rect)

        


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['mana'], self.mana_bar_rect, MANA_COLOR)

        self.show_exp(player.exp)

        self.spell_box(10, 630, self.spell_img[0], player.fireball_cooldown, "Space", spell_data["fireball"]["mana"])
        self.spell_box(SPELL_BOX_SIZE + 20, 630, self.spell_img[1], player.laserbeam_cooldown, "Q", spell_data["laserbeam"]["mana"],  player.get_cooldown_time("laserbeam"))
        self.spell_box(2*SPELL_BOX_SIZE + 30, 630, self.spell_img[2], False, "E", spell_data["heal"]["mana"], player.get_cooldown_time("laserbeam"))