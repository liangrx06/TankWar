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


class Wall():
    def __init__(self):
        self.homewallGroup  = pygame.sprite.Group()
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup  = pygame.sprite.Group()
        self.wallGroups = [self.homewallGroup, self.brickGroup, self.ironGroup]
        
        # 数字代表地图中的位置
        # home
        self.homewall = [([11, 14], [23, 24, 25]), ([12, 13], [23])]
        # 其他砖块
        XY1379 = ([2, 3, 6, 7, 18, 19, 22, 23], [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23])
        XY28 = ([10, 11, 14, 15], [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20])
        XY46 = ([4, 5, 6, 7, 18, 19, 20, 21], [13, 14])
        XY5  = ([12, 13], [16, 17])
        self.other_bricks = [XY1379, XY28, XY46, XY5]
        # 石头
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
                    elif walltype == 2:
                        wall = Iron()
                    wall.rect.left, wall.rect.top = 3 + x * 24, 3 + y * 24
                    for wall_group in groups:
                        wall_group.add(wall)

            
        