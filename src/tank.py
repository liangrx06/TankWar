import pygame
import random

from settings import *
from bullet import Bullet


tank_T1_0 = r"..\image\tank_T1_0.png"
tank_T1_1 = r"..\image\tank_T1_1.png"
tank_T1_2 = r"..\image\tank_T1_2.png"
tank_T2_0 = r"..\image\tank_T2_0.png"
tank_T2_1 = r"..\image\tank_T2_1.png"
tank_T2_2 = r"..\image\tank_T2_2.png"


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, side = 1, kind = None, enemy_pos = None):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.side = side # 1表示己方坦克，2表示敌方坦克
        # 参数:坦克种类
        self.kind = kind
        if kind is None:
            self.kind = random.choice([1, 2, 3, 4])

        if self.side == 1:
            self.life = 3
        else:
            self.life = 1
            if self.kind == 3:
                self.life = 3

        # 参数：敌方坦克位置
        self.pos = enemy_pos
        if not self.pos:
            self.pos = random.choice([1, 2, 3])
        self.pos -= 1

        self.all_levels_images = []
        for i in range(4):
            ss = r"\tank_T" if self.side == 1 else r"\enemy_"
            file = r"..\image" + ss + str(self.kind) + "_" + str(i) + ".png"
            # print(file)
            self.all_levels_images.append(pygame.image.load(file).convert_alpha())
        self.enemy_3_0 = pygame.image.load(r"..\image\enemy_3_0.png").convert_alpha()
        self.enemy_3_2 = pygame.image.load(r"..\image\enemy_3_2.png").convert_alpha()

        self.bullet = Bullet(self)

        # 坦克出现动画
        appearing_image = pygame.image.load(r"..\image\appear.png").convert_alpha()
        self.appearing = []
        self.appearing.append(appearing_image.subsurface((0, 0), (48, 48)))
        self.appearing.append(appearing_image.subsurface((48, 0), (48, 48)))
        self.appearing.append(appearing_image.subsurface((96, 0), (48, 48)))

        # 坦克保护罩动画
        protect_image = pygame.image.load(r"..\image\protect.png").convert_alpha()
        self.protect = []
        self.protect.append(protect_image.subsurface((0, 0), (48, 48)))
        self.protect.append(protect_image.subsurface((48, 0), (48, 48)))
        
        self.init_new_life()

    def init_new_life(self):
        self.time_tick = 0

        self.appearing_time = 90 # 单位为1/60秒

        self.protect_time = 0

        if self.side == 1:
            self.dir = self.old_dir = 0
        else:
            self.dir = self.old_dir = 1

        self.bulletNotCooling = True

        self.rect = pygame.Rect(0, 0, 48, 48)
        if self.side == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8 * self.kind, 3 + 24 * 24
        else:
            self.rect.left, self.rect.top = 3 + self.pos * 12 * 24, 3 + 0 * 24

        # 坦克的四个等级，初始坦克为0级
        self.level = 0
        if self.side == 2:
            isred = random.choice((True, False, False, False, False)) # 参数:是否携带食物
            if isred:
                self.level = 3
        self.init_by_level()

    def init_by_level(self):
        # 坦克速度 图片 运动 子弹
        if self.side == 1:
            speeds = [3, 3, 3, 24]
            self.speed = speeds[self.level]
        else:
            self.speed = 1
            if self.kind == 2:
                self.speed = 3

        self.init_moving()

        self.init_bullet()

    def init_bullet(self):
        if self.side == 1:
            bullet_speeds = [6, 16, 16, 48]
            bullet_strongs = [False, False, True, True]
            self.bullet.speed = bullet_speeds[self.level]
            self.bullet.strong = bullet_strongs[self.level]

    def init_moving(self):
        self.moving = False
        # 运动中的两种图片
        self.level_images = self.all_levels_images[self.level]
        self.change_dir(self.dir)

    def levelTo(self, level = 0):
        if level < 0 or level > 3:
            level = 0
        self.level = level
        self.init_by_level()

    def levelUp(self):
        if self.level < 2:
            self.level += 1
        self.init_by_level()

    def levelDown(self):
        if self.level == 0:
            self.life -= 1
            self.init_new_life()
        else:
            if self.level == 3 and self.side == 2:
                self.level = 0
            else:
                self.level -= 1
            self.init_by_level()

    def print(self):
        print('Player', self.kind, ': level', self.level, ', speed', self.speed, ', bullet_speed', self.bullet.speed,
              ', moving', self.moving, ', life', self.life, ', rect_x', self.rect.x, ', rect_y', self.rect.y)

    def shoot(self):
        # 子弹
        self.bullet.life = True
        self.init_bullet()
        self.bullet.changeImage(self.dir)
        self.bullet.changeLocation(self.dir)
        self.game.bulletGroups[self.side - 1].add(self.bullet)

    def moveUp(self, objectGroups):
        self.change_dir(0)
        return self.move(objectGroups)

    def moveDown(self, objectGroups):
        self.change_dir(1)
        return self.move(objectGroups)

    def moveLeft(self, objectGroups):
        self.change_dir(2)
        return self.move(objectGroups)

    def moveRight(self, objectGroups):
        self.change_dir(3)
        return self.move(objectGroups)

    def get_image(self, index = 0):
        return self.level_images.subsurface((index * 48, self.dir * 48), (48, 48))

    def change_dir(self, dir):
        self.old_dir = self.dir
        self.dir = dir
        self.images = [self.get_image(0), self.get_image(1)]

    # 返回True 代表发生碰撞
    def move(self, objectGroups):
        allGroup = pygame.sprite.Group()
        for group in objectGroups:
            for object in group:
                allGroup.add(object)
        allGroup.remove(self)
        dir_x, dir_y = DIRS[self.dir]
        self.rect = self.rect.move(self.speed * dir_x, self.speed * dir_y)
        if self.rect.top < 3 or self.rect.bottom > 630 - 3 \
                or self.rect.left < 3 or self.rect.right > 630 - 3 \
                or pygame.sprite.spritecollide(self, allGroup, False, None):
            self.rect = self.rect.move(-self.speed * dir_x, -self.speed * dir_y)
            if self.side == 2: #随机改变方向
                self.change_dir(random.choice(range(0, 4)))
            return True
        return False

    def check_life(self):
        return self.life > 0

    def check_living(self):
        return self.appearing_time == 0

    def check_appearing(self):
        return self.appearing_time > 0

    def check_protect(self):
        return self.protect_time > 0

    def set_protect(self, protect_time=600):
        self.protect_time = protect_time

    def appearing_flash(self, screen):
        # 播放坦克出现5毛钱特效
        if self.appearing_time > 0:
            self.appearing_time -= 1
            screen.blit(self.appearing[self.appearing_time // 10 % 3], self.rect)

    def protect_flash(self, screen):
        # 播放坦克保护罩5毛钱特效
        if self.protect_time > 0:
            self.protect_time -= 1
            screen.blit(self.protect[self.protect_time // 10 % 2], self.rect)

    def draw_tank(self, screen):
        if self.life:
            if self.moving or self.side == 2:
                screen.blit(self.images[self.time_tick // 5 % 2], (self.rect.left, self.rect.top))
            else:
                screen.blit(self.images[0], (self.rect.left, self.rect.top))
            if self.check_protect():
                self.protect_flash(screen)

    def do_time_tick(self):
        self.time_tick += 1