import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

from lift import Lift
import config as c
from game import Game

class StackAttack(Game):
    def __init__(self):
        Game.__init__(self, 'StackAttack', c.screen_width, c.screen_height, c.background_image, c.frame_rate)
        self.lift = None

        self.create_objects()
        

    def create_objects(self):
        self.create_lift()

    def handle_collisions(self):
        pass

    def create_lift(self):
        lift = Lift(-c.lift_width,
                    0,
                    c.lift_width,
                    c.lift_height,
                    c.lift_color,
                    c.lift_speed)
        self.lift = lift
        self.objects.append(self.lift)


    def update(self):
        self.handle_collisions()
        super().update()

def main():
    StackAttack().run() 


if __name__ == '__main__':
    main()
