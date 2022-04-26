import pygame
from pygame.sprite import Sprite

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank = None):
        pygame.sprite.Sprite.__init__(self)

        self.tank = tank
        
        bullet_up = pygame.image.load(r"..\image\bullet_up.png")
        bullet_down = pygame.image.load(r"..\image\bullet_down.png")
        bullet_left = pygame.image.load(r"..\image\bullet_left.png")
        bullet_right = pygame.image.load(r"..\image\bullet_right.png")
        self.bullet_images = [bullet_up, bullet_down, bullet_left, bullet_right]

        # 子弹方向   速度   生命   碎石
        self.dir = 0
        self.speed  = 6
        self.strong = False

        self.image = self.bullet_images[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
    
    def changeImage(self, dir):
        self.dir = dir
        self.image = self.bullet_images[dir]
        self.rect = self.image.get_rect()

    def changeLocation(self, dir):
        self.dir = dir
        if self.dir == 0:
            self.rect.left = self.tank.rect.left + 18
            self.rect.bottom = self.tank.rect.top + 1
        elif self.dir == 1:
            self.rect.left = self.tank.rect.left + 18
            self.rect.top = self.tank.rect.bottom - 1
        elif self.dir == 2:
            self.rect.right = self.tank.rect.left - 1
            self.rect.top = self.tank.rect.top + 18
        elif self.dir == 3:
            self.rect.left = self.tank.rect.right + 1
            self.rect.top = self.tank.rect.top + 18
    
    def move(self):
        dir_x, dir_y = DIRS[self.dir]
        self.rect = self.rect.move(self.speed * dir_x, self.speed * dir_y)