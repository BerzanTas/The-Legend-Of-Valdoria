import pygame
from settings import *

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/portal.png").convert_alpha()
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_speed = 100  # ms between frames
        self.last_update = pygame.time.get_ticks()

    def load_frames(self):
        frames = []
        for i in range(8):
            frame = self.get_sprite(self.sprite_sheet, i, 0, 64, 64)
            frames.append(frame)
        return frames

    def get_sprite(self, sheet, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width, y * height, width, height))
        return image

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

############klasa water#############
class Water(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.sprite_sheet = pygame.image.load("img/water-sheet.png").convert_alpha()
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_speed = 100  # ms between frames
        self.last_update = pygame.time.get_ticks()
        self.hitbox = self.rect.inflate(-20, -20)  #hitbox

    def load_frames(self):
        frames = []
        frame_width = 45
        frame_height = 45
        spacing = 35
        for i in range(6):
            frame = self.get_sprite(self.sprite_sheet, i * (frame_width + spacing), 0, frame_width, frame_height)
            frames.append(frame)
        return frames

    def get_sprite(self, sheet, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x, y, width, height))
        return image

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
