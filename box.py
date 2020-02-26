from pygame import *
import config as c
import random

WIDTH = 40
HEIGHT = 40
COLOR =  "#0000FF"
GRAVITY = 0.35# Сила, которая будет тянуть нас вниз


class Box(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект 

        self.has_border_collision = False
        self.has_box_collision = (False, False, False, False) # has any collision, left, right topo
        self.has_player_collision = False

    def check_collision(self, player, boxes):
        self.has_border_collision = self.has_collide_with_borders()
        self.has_box_collision = self.has_collide_with_box(boxes) 
        self.has_player_collision = self.has_collide_with_player(player)   

    def update(self, player=None, boxes=None):       
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False; # Мы не знаем, когда мы на земле((   
        self.rect.y += self.yvel

        self.collide_with_player(0, self.yvel, player)
        self.collide_with_boxes(0, self.yvel, boxes, player)
        self.collide_with_borders()

    def has_collide_with_borders(self):
        if self.rect.left == 0 or self.rect.right == c.screen_width:
            return True

        return False

    def has_collide_with_box(self, boxes):
        if not boxes:
            return (False, False, False, False)

        for b in boxes:
            if self == b:
                continue
            if sprite.collide_rect(self, b):
                has_from_left = False
                has_from_right = False
                has_from_top = False
                if b.rect.right > self.rect.right and b.rect.top == self.rect.top:
                    has_from_right = True
                if b.rect.left < self.rect.left and b.rect.top == self.rect.top:
                    has_from_left = True
                if self.yvel > 0 and self.rect.top < b.rect.top:
                    has_from_top = True

                return (True, has_from_left, has_from_right, has_from_top)

        return (False, False, False, False)

    def has_collide_with_player(self, player):
        if not player:
            return False

        if sprite.collide_rect(self, player) or self.rect.left == player.rect.right or self.rect.right == player.rect.left:
            return True
    
        return False

    def collide_with_borders(self):
        collisions = False
        if self.rect.bottom > c.screen_height:
            self.onGround = True
            self.yvel = 0 
            self.rect.bottom = c.screen_height     
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= c.screen_width:
            self.rect.right = c.screen_width
    
    def collide_with_boxes(self, xvel, yvel, boxes, player):
        if not boxes:
            return
        for b in boxes:
            if (self == b):
                continue

            if sprite.collide_rect(self, b): # если есть пересечение платформы с ящиком
                if yvel > 0 and self.rect.top < b.rect.top: # если падает вниз
                    self.rect.bottom = b.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает
                if self.has_box_collision[1] and self.has_player_collision:
                    self.rect.left = b.rect.right
                    player.rect.left = self.rect.right

                if self.has_box_collision[2] and self.has_player_collision:
                    self.rect.right = b.rect.left
                    player.rect.right = self.rect.left

    def collide_with_player(self, xvel, yvel, player):
        if not player:
            return

        if sprite.collide_rect(self, player):
            if player.xvel > 0 and not self.has_border_collision and not self.has_box_collision[2] and not self.has_box_collision[3]:                    
                self.rect.left = player.rect.right

            if player.xvel < 0 and not self.has_border_collision and not self.has_box_collision[1] and not self.has_box_collision[3]:                
                self.rect.right = player.rect.left  

            if self.rect.top < player.rect.top: 
                ##### GAME OVER #####  
                exit()      
    