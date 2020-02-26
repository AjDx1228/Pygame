from pygame import *
import config as c

MOVE_SPEED = 10
WIDTH = 80
HEIGHT = 20
COLOR =  "#FF0000"

class Lift(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = MOVE_SPEED   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект 

    def update(self):
        self.rect.x += self.xvel

