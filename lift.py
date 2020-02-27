from pygame import *
import pygame
import config as c

MOVE_SPEED = 5
WIDTH = 280
HEIGHT = 40
COLOR =  "#FF0000"

class Lift(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = MOVE_SPEED   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = image.load("images/lift.png")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект 

    def update(self):
        self.rect.x += self.xvel

