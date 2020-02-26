from pygame import *
import config as c
MOVE_SPEED = 10
WIDTH = 20
HEIGHT = 40
COLOR =  "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект 

        self.left = False 
        self.right = False
        self.up = False
        self.has_border_collision = True
        self.has_box_collision = False

    def handle_keyup(self, key):
        if key == K_UP:
            self.up = False
        if key == K_RIGHT:
            self.right = False
        if key == K_LEFT:
            self.left = False

    def handle_keydown(self, key):
        if key == K_UP:
            self.up = True
        if key == K_LEFT:
            self.left = True
        if key == K_RIGHT:
            self.right = True

    def has_collide_with_borders(self):
        if self.rect.bottom > c.screen_height or self.rect.left < 0 or self.rect.right > c.screen_width:
            return True

        return False

    def has_collide_with_box(self, boxes):
        if not boxes:
            return False

        for b in boxes:
            if sprite.collide_rect(self, b):
                return True

        return False


    def check_collision(self, boxes):
        self.has_border_collision = self.has_collide_with_borders()
        self.has_box_collision = self.has_collide_with_box(boxes)

    def update(self, boxes=None):
        if self.up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                             
        if self.left:
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if self.right:
            self.xvel = MOVE_SPEED # Право = x + n
         
        if not(self.left or self.right): # стоим, когда нет указаний идти
            self.xvel = 0
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False  
        self.onBox = False 
        self.rect.y += self.yvel
        self.rect.x += self.xvel 

        self.collide_with_boxes(self.xvel, self.yvel, boxes)
        self.collide_with_borders()
   
    def collide_with_borders(self):
        if self.rect.bottom > c.screen_height:
            self.onGround = True
            self.yvel = 0 
            self.rect.bottom = c.screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > c.screen_width:
            self.rect.right = c.screen_width

    def collide_with_boxes(self, xvel, yvel, boxes):
        if not boxes:
            return
        for b in boxes:
            if sprite.collide_rect(self, b):
                if yvel != 0 and self.rect.top < b.rect.top:
                    self.rect.bottom = b.rect.top
                    self.onGround = True 
                    self.onBox = True       
                    self.yvel = 0 

                if self.xvel > 0 and not self.onBox and (b.has_border_collision or b.has_box_collision[2] or b.has_box_collision[3]):                  
                    self.rect.right = b.rect.left

                if self.xvel < 0 and not self.onBox and (b.has_border_collision or b.has_box_collision[1] or b.has_box_collision[3]):         
                    self.rect.left = b.rect.right         