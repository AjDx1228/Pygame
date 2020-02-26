import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

from pygame import *
from lift import Lift
import config as c
from player import Player
from border import Border
from game import Game
from box import Box

class StackAttack(Game, sprite.Sprite):
    def __init__(self):
        Game.__init__(self, 'StackAttack', c.screen_width, c.screen_height, c.background_image, c.frame_rate)

        self.boxes = []
        self.create_objects()
        
    def create_objects(self):
        self.create_lift()
        self.create_player()
        self.create_box()


    def handle_collisions(self):
        # Передвижение лифта и создание новой коробки
        if self.lift.rect.x >= c.screen_width:
            self.lift.rect.x = self.lift.startX
            self.create_box()
        

         # Двигаем коробку вместе с краном до рандомной зоны
        if self.box and self.box.rect.right < self.random_zone * c.box_width:
            self.box.rect.left = self.lift.rect.left
            self.box.yvel = 0
        elif self.box:
            self.boxes.append(self.box)
            self.box = None
        
        count = 0
        for box in self.boxes:
            if box.rect.bottom == c.screen_height:
                count += 1
                if count == c.n_zones:
                    break
        
        if count == c.n_zones:
            for box in self.boxes:
                if box.rect.bottom == c.screen_height:
                    self.entities.remove(box)
                    self.boxes.remove(box)

    
    def create_box(self): 
        self.random_zone = random.randint(1, c.n_zones)
        self.box = Box(self.lift.rect.x, c.lift_height)
        self.entities.add(self.box)

    def create_lift(self):
        self.lift = Lift(-c.lift_width, 0)
        self.entities.add(self.lift)

    def create_player(self):
        self.player = Player(50, 50)
        self.keydown_handlers[pygame.K_LEFT].append(self.player.handle_keydown)
        self.keydown_handlers[pygame.K_RIGHT].append(self.player.handle_keydown)
        self.keydown_handlers[pygame.K_UP].append(self.player.handle_keydown)
        self.keyup_handlers[pygame.K_LEFT].append(self.player.handle_keyup)
        self.keyup_handlers[pygame.K_RIGHT].append(self.player.handle_keyup)
        self.keyup_handlers[pygame.K_UP].append(self.player.handle_keyup)
        self.entities.add(self.player)

    def update(self):
        super().update()
        # Установка флагов коллизий
        self.player.check_collision(self.boxes)
        for box in self.boxes:
            box.check_collision(self.player, self.boxes)

        self.handle_collisions()

        self.lift.update()
        if self.box:
            self.box.update()
            
        self.player.update(self.boxes)
        for box in self.boxes:
            box.update(self.player, self.boxes)




def main():
    StackAttack().run() 

if __name__ == '__main__':
    main()
