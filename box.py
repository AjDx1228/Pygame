import pygame
import random

import config as c
from game_object import GameObject


class Box(GameObject):
    def __init__(self, x, y, w, h, color, offset, random_zone):
        GameObject.__init__(self, x, y, w, h)
        self.start_position = x
        self.color = color
        self.offset = offset
        self.random_zone = random_zone
        self.zone = c.zones[self.random_zone]
        c.zones[self.random_zone] += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self):
        if self.left == c.box_width * (self.random_zone - 1) and self.bottom != c.screen_height - self.zone * c.box_height:
            dx = 0
            dy = 5
        elif self.bottom == c.screen_height - self.zone * c.box_height:
            dx = 0
            dy = 0
        else:
            dx = self.offset
            dy = 0

        self.move(dx, dy)