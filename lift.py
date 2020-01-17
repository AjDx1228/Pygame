import pygame

import config as c
from game_object import GameObject


class Lift(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.start_position = x
        self.color = color
        self.offset = offset

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        pass

    def update(self):
        if self.left >= c.screen_width:
            self.move(-c.screen_width + self.start_position, 0)
            return

        dx = self.offset
        self.move(dx, 0)
