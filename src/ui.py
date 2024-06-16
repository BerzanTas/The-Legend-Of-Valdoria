import pygame
import pygame.locals
from settings import *
from projectile import *

class UI:
    def __init__(self) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.exp_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.bar_font = pygame.font.Font(UI_FONT, 14)
        self.spell_font = pygame.font.Font(SPELL_FONT, 20)
        self.cooldown_font = pygame.font.FontType(UI_FONT, 28)

        # bar
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(10, 34, MANA_BAR_WIDTH, BAR_HEIGHT)
        self.experience_rect = pygame.Rect(1060, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        self.stat_box_x = 940

        self.mouse_was_pressed = False

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

        text_surf = self.bar_font.render(str(str(int(current))+"/"+str(int(max_amount))), False, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.topright = bg_rect.topright
        
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        self.display_surface.blit(text_surf, text_rect)


    def show_exp(self, exp, max_exp, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # zmiana statów na piksele
        ratio = exp / max_exp
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        text_surf = self.bar_font.render(str(str(int(exp))+"/"+str(int(max_exp))), False, TEXT_COLOR)
        text_rect = text_surf.get_rect()
        text_rect.center = bg_rect.center
        
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        self.display_surface.blit(text_surf, text_rect)

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

    
    def stat_box(self, left, top, stat_name, path):
        bg_rect = pygame.Rect(left, top, STAT_BOX_SIZE, STAT_BOX_SIZE)
        stat_img = pygame.image.load(path)
        stat_rect = stat_img.get_rect(center = bg_rect.center)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        self.display_surface.blit(stat_img, stat_rect)
    
    def upgrade_box(self, pos, skill, player):
        path = "img/staticons/statup.png"
        image = pygame.image.load(path).convert_alpha()
        img_rect = image.get_rect(topleft = pos)

        self.display_surface.blit(image, img_rect)

        if self.mouse_clicked and not self.mouse_was_pressed:
            x,y = pygame.mouse.get_pos()
            if img_rect.collidepoint(x, y):
                player.upgrade(skill)
                print("upgrade")


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['mana'], self.mana_bar_rect, MANA_COLOR)

        self.show_exp(player.exp, player.next_level_exp, self.experience_rect, EXP_COLOR)

        self.spell_box(10, 640, self.spell_img[0], player.fireball_cooldown, "Space", spell_data["fireball"]["mana"])
        self.spell_box(SPELL_BOX_SIZE + 20, 640, self.spell_img[1], player.laserbeam_cooldown, "Q", spell_data["laserbeam"]["mana"],  player.get_cooldown_time("laserbeam"))
        self.spell_box(2*SPELL_BOX_SIZE + 30, 640, self.spell_img[2], player.heal_cooldown, "E", spell_data["heal"]["mana"], player.get_cooldown_time("heal"))

        self.stat_box(self.stat_box_x, 660, "Health", "img/staticons/healthicon.png")
        self.stat_box(self.stat_box_x + STAT_BOX_SIZE + 5, 660, "Health Regen", "img/staticons/healthregenicon.png")
        self.stat_box(self.stat_box_x + 2*STAT_BOX_SIZE + 10, 660, "Mana", "img/staticons/manaicon.png")
        self.stat_box(self.stat_box_x + 3*STAT_BOX_SIZE + 15, 660, "Mana Regen", "img/staticons/manaregenicon.png")
        self.stat_box(self.stat_box_x + 4*STAT_BOX_SIZE + 20, 660, "Magic Power", "img/staticons/strenghticon.png")
        self.stat_box(self.stat_box_x + 5*STAT_BOX_SIZE + 25, 660, "Speed", "img/staticons/speedicon.png")

        self.mouse_clicked = pygame.mouse.get_pressed()[0]
        if player.ability_points > 0:
            if player.stats['health'] < player.max_stats['health']:
                self.upgrade_box((self.stat_box_x + 6, 625), 'health', player)
            if player.stats['health_regen'] < player.max_stats['health_regen']:
                self.upgrade_box((self.stat_box_x + STAT_BOX_SIZE + 13, 625), 'health_regen', player)
            if player.stats['mana'] < player.max_stats['mana']:
                self.upgrade_box((self.stat_box_x + 2*STAT_BOX_SIZE + 18, 625), 'mana', player)
            if player.stats['mana_regen'] < player.max_stats['mana_regen']:
                self.upgrade_box((self.stat_box_x + 3*STAT_BOX_SIZE + 23, 625), 'mana_regen', player)
            if player.stats['magic'] < player.max_stats['magic']:
                self.upgrade_box((self.stat_box_x + 4*STAT_BOX_SIZE + 28, 625), 'magic', player)
            if player.stats['speed'] < player.max_stats['speed']:
                self.upgrade_box((self.stat_box_x + 5*STAT_BOX_SIZE + 33, 625), 'speed', player)
        self.mouse_was_pressed = self.mouse_clicked

class StartMenu:
    def __init__(self) -> None:
        self.box_width = 300
        self.box_height = 60

        self.bg = pygame.image.load("img/assets/menu.png")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGTH))
        self.text_color = '#fc4f53'

        self.display_surface = pygame.display.get_surface()

        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('#fc4f53')
        self.color = self.color_inactive

        self.active = False
        self.username = 'Username'
        self.can_write = True

        self.font = pygame.font.Font(UI_FONT, 34)
        self.x = 490
        self.y = 270
        self.username_input = pygame.Rect(self.x, self.y, self.box_width, self.box_height)

    def menu_box(self, text: str, x, y, events):
        bg_rect = pygame.Rect(x+10, y, self.box_width-20, self.box_height)

        if bg_rect.collidepoint(pygame.mouse.get_pos()):
            text = self.font.render(text, True, 'white')
            pygame.draw.rect(self.display_surface, self.text_color, bg_rect)
        else:
            text = self.font.render(text, True, self.text_color)
            pygame.draw.rect(self.display_surface, self.text_color, bg_rect, 3)

        text_rect = text.get_rect(center=bg_rect.center)
        self.display_surface.blit(text, text_rect)

        return bg_rect

    def get_input(self, input_box, events):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                    if self.username == 'Username':
                        self.username = ''
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.color_active if self.active else self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print(self.username)
                        self.username = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if self.can_write:
                            self.username += event.unicode

        txt_surface = self.font.render(self.username, True, self.color)
        txt_rect = txt_surface.get_rect(center=input_box.center)
        self.display_surface.blit(txt_surface, txt_rect)
        pygame.draw.rect(self.display_surface, self.color, input_box, 2)

        if txt_rect.width >= input_box.width-30:
            self.can_write = False
        else:
            self.can_write = True


    def display(self, events):
        self.display_surface.blit(self.bg, (0,0))

        self.get_input(self.username_input, events)
        start_button = self.menu_box("Start", self.x,self.y+80, events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and len(self.username) >= 3:
                    return True
        



class End():
    pass