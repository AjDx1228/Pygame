from pygame import *
import pygame
import config as c
import pyganim

MOVE_SPEED = 10
WIDTH = 25
HEIGHT = 40
COLOR =  "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 1 # скорость смены кадров

ANIMATION_RIGHT = ['images/r1.png',
            'images/r2.png',
            'images/r3.png',
            'images/r4.png',
            'images/r5.png']
ANIMATION_LEFT = ['images/l1.png',
            'images/l2.png',
            'images/l3.png',
            'images/l4.png',
            'images/l5.png']
ANIMATION_IDE = [('images/0.png', ANIMATION_DELAY)]

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
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект 

        self.left = False 
        self.right = False
        self.up = False
        self.has_border_collision = True
        self.has_box_collision = False

        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.scale((WIDTH,HEIGHT))
        self.boltAnimRight.play()
        #        Анимация движения влево        
        boltAnim = []

        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.scale((WIDTH,HEIGHT))
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_IDE)
        self.boltAnimStay.scale((WIDTH,HEIGHT))
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим

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
            self.image.fill(Color(COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
 
        if self.right:
            self.image.fill(Color(COLOR))
            self.xvel = MOVE_SPEED # Право = x + n
            self.boltAnimRight.blit(self.image, (0, 0))
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

         
        if not(self.left or self.right): # стоим, когда нет указаний идти
            self.xvel = 0
            self.image.fill(Color(COLOR))
            self.boltAnimStay.blit(self.image, (0, 0))
            self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            
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