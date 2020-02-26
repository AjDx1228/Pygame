from pygame import *

COLOR = "#FF6262"
 
class Border(sprite.Sprite):
    def __init__(self, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.image = Surface((w, h))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, w, h)   