import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

from lift import Lift
import config as c
from player import Player
from game import Game
from box import Box

class StackAttack(Game):
    def __init__(self):
        Game.__init__(self, 'StackAttack', c.screen_width, c.screen_height, c.background_image, c.frame_rate)
        self.lift = None

        self.create_objects()
        
    def create_objects(self):
        self.create_lift()
        self.create_player()
        self.create_box()

    def handle_collisions(self):
        if self.lift.left >= c.screen_width:
            self.lift.set_reset_flag(True)
            self.create_box()
            return
    
    def create_box(self):
        zones = c.screen_width / c.box_width
        random_zone = random.randint(1, zones)
        box = Box(-c.lift_width + c.lift_width / 4,
                    c.lift_height,
                    c.box_width,
                    c.box_height,
                    c.box_color,
                    c.box_speed,
                    random_zone)
        self.box = box
        self.objects.append(self.box) 

    def create_lift(self):
        lift = Lift(-c.lift_width,
                    0,
                    c.lift_width,
                    c.lift_height,
                    c.lift_color,
                    c.lift_speed)
        self.lift = lift
        self.objects.append(self.lift)

    def create_player(self):
        player = Player((c.screen_width - c.player_width) // 2,
                        c.screen_height - c.player_height,
                        c.player_width,
                        c.player_height,
                        c.player_color,
                        c.player_speed)
        self.keydown_handlers[pygame.K_LEFT].append(player.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(player.handle)
        self.keyup_handlers[pygame.K_LEFT].append(player.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(player.handle)
        self.keydown_handlers[pygame.K_UP].append(player.handle)
        self.player = player
        self.objects.append(self.player)


    def update(self):
        self.handle_collisions()
        super().update()


def main():
    StackAttack().run() 

if __name__ == '__main__':
    main()
