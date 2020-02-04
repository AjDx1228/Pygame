import pygame

import config as c
from game_object import GameObject

from box import Box


class Lift(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.start_position = x
        self.color = color
        self.offset = offset
        self.reset_flag = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        pass

    def update(self):
        if self.reset_flag:
            self.move(-c.screen_width + self.start_position, 0)
            self.reset_flag = False
            return

        dx = self.offset
        self.move(dx, 0)
    
    def set_reset_flag(self, value):
        self.reset_flag = value

