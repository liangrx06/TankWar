# -*- coding:GBK -*-

import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        brickImage = r"..\image\brick.png"
        self.image = pygame.image.load(brickImage)
        self.rect = self.image.get_rect()


class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ironImage = r"..\image\iron.png"
        self.image = pygame.image.load(ironImage)
        self.rect = self.image.get_rect()


class Home(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.life = True

        homeImage = r"..\image\home.png"
        homeImage1 = r"..\image\home1.png"
        homeDestroyedImage = r"..\image\home_destroyed.png"
        self.image = pygame.image.load(homeImage1)
        self.image_destroyed = pygame.image.load(homeDestroyedImage)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)

class Wall():
    def __init__(self, game):
        self.game = game

        self.homewallGroup  = pygame.sprite.Group()
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup  = pygame.sprite.Group()
        self.wallGroups = [self.homewallGroup, self.brickGroup, self.ironGroup]
        
        # ���ִ����ͼ�е�λ��
        # home
        self.homewall = [([11, 14], [23, 24, 25]), ([12, 13], [23])]
        # ����ש��brick
        XY1379 = ([2, 3, 6, 7, 18, 19, 22, 23], [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23])
        XY28 = ([10, 11, 14, 15], [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20])
        XY46 = ([4, 5, 6, 7, 18, 19, 20, 21], [13, 14])
        XY5  = ([12, 13], [16, 17])
        self.other_bricks = [XY1379, XY28, XY46, XY5]
        # ʯͷiron
        self.irons = [([0, 1, 24, 25], [14]), ([12, 13], [6, 7])]

        self.draw_wall()

    def draw_wall(self):
        self.draw_homewall(1)
        self.draw(1, [self.brickGroup], self.other_bricks)
        self.draw(2, [self.ironGroup], self.irons)

    def draw_homewall(self, walltype = 1):
        for wall in self.homewallGroup.copy():
            for wall_group in self.wallGroups:
                if wall in wall_group:
                    wall_group.remove(wall)
        if walltype == 1:
            self.draw(1, [self.brickGroup, self.homewallGroup], self.homewall)
        elif walltype == 2:
            self.draw(2, [self.ironGroup, self.homewallGroup], self.homewall)

    def draw(self, walltype, groups, locations):
        for XY in locations:
            for x in XY[0]:
                for y in XY[1]:
                    if walltype == 1:
                        wall = Brick()
                    else:
                        wall = Iron()
                    wall.rect.left, wall.rect.top = 3 + x * 24, 3 + y * 24
                    for wall_group in groups:
                        wall_group.add(wall)

            
        