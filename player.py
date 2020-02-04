import pygame

import config as c
from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False

        self.jump = False
        self.jump_flag = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        if key == pygame.K_UP:
            self.jump = True
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        if key == pygame.K_RIGHT:
            self.moving_right = not self.moving_right
    
    def jump_and_move(self, dx, bottom_now):
        if self.bottom != c.screen_height - bottom_now - c.player_height - 70 and not self.jump_flag:
            dy = 5
        else:
            self.jump_flag = True
            dy = -10
            if self.bottom == c.screen_height - bottom_now - (c.player_height - c.box_height):
                self.jump_flag = False
                self.jump = False
        self.move(dx, -dy)

    def update(self):
        self.zone = (self.left // c.box_width) + 1
        if self.zone != 1 and self.zone != c.n_zones:
            box_left = c.zones[self.zone - 1]
            box_right = c.zones[self.zone + 1]
        elif self.zone == 1:
            box_left = 100
            box_right = c.zones[self.zone + 1]
        else:
            box_right = 100
            box_left = c.zones[self.zone - 1] 

        if self.jump and self.moving_left:
            self.jump_and_move(-(min(self.offset, self.left)), c.box_height * box_left)

        elif self.jump and self.moving_right:
            self.jump_and_move((min(self.offset, c.screen_width - self.right)), c.box_height * box_right)

        elif self.jump:
            self.jump_and_move(0, c.box_height * c.zones[self.zone])

        elif self.moving_left and box_left - c.zones[self.zone] != 1:
                dx, dy = -(min(self.offset, self.left)), 0
                self.move(dx, -dy)

        elif self.moving_right and box_right - c.zones[self.zone] != 1:
            dx, dy = min(self.offset, c.screen_width - self.right), 0
            self.move(dx, -dy)

        else:
            return 
