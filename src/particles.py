import pygame
from itertools import chain

class AnimationPlayer:
    def __init__(self) -> None:
        self.heal_sprite = pygame.image.load("img/spells/heal.png")
        self.frames = {
            'heal': [self.create_animation(self.heal_sprite, 0, 5, 192, 192),
                     self.create_animation(self.heal_sprite, 1, 5, 192, 192),
                     self.create_animation(self.heal_sprite, 2, 5, 192, 192)]
        }

    def get_sprite(self, sheet, x, y, width, height, offset = 0):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (x * width + offset, y * height, width, height))
        return image

    def create_animation(self, sheet, row, num_frames, width, heigth):
        return [self.get_sprite(sheet, i, row, width, heigth) for i in range(num_frames)]

    def create_healing_particles(self, pos, groups):
        animation_frames = list(chain.from_iterable(self.frames['heal']))
        Particle(pos, animation_frames, groups)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()