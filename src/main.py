import pygame
import sys
import traceback

from wall import Wall
from tank import Tank
from bullet import Bullet
from food import Food

from settings import *


class TankWar():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(RESOLUTION)
        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Tank War")
        # 游戏窗口下鼠标不可见
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        self.enemyCouldMove = True
        self.homeSurvive = True

        self.init_images()

        self.init_sounds()

        self.user_loop_events()

        self.init_groups()

        self.init_bgmap()

        self.init_food()

        self.init_tank(side=1)
        self.init_tank(side=2)

    def init_groups(self):
        # 定义精灵组:我方坦克，敌方坦克，敌方子弹
        self.playerGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.redEnemyGroup = pygame.sprite.Group()
        self.greenEnemyGroup = pygame.sprite.Group()
        self.otherEnemyGroup = pygame.sprite.Group()

        self.playerBulletGroup = pygame.sprite.Group()
        self.enemyBulletGroup = pygame.sprite.Group()

        self.tankGroups = [self.playerGroup, self.enemyGroup]
        self.bulletGroups = [self.playerBulletGroup, self.enemyBulletGroup]

    def init_bgmap(self):
        # 创建地图
        self.bgMap = Wall()
        self.objectGroups = [self.playerGroup, self.enemyGroup, self.bgMap.brickGroup, self.bgMap.ironGroup]

    def init_food(self):
        # 创建食物/道具 但不显示
        self.food = Food()

    def init_tank(self, side=1):
        if side == 1:  # 创建我方坦克
            self.myTank = []
            for i in range(2):
                self.myTank.append(Tank(self, side=1, kind=i + 1))
                self.playerGroup.add(self.myTank[i])
        else:  # 创建敌方 坦克
            for i in range(1, 4):
                self.init_enemy_tank(i)

    def init_enemy_tank(self, enemy_pos=None):
        enemy = Tank(self, side=2, enemy_pos=enemy_pos)
        self.enemyGroup.add(enemy)
        if enemy.level == 3:
            self.redEnemyGroup.add(enemy)
        elif enemy.kind == 3:
            self.greenEnemyGroup.add(enemy)
        else:
            self.otherEnemyGroup.add(enemy)

    def init_images(self):
        self.background_image = pygame.image.load(r"..\image\background.png")
        self.home_image = pygame.image.load(r"..\image\home.png")
        self.home_destroyed_image = pygame.image.load(r"..\image\home_destroyed.png")

    def init_sounds(self):
        self.start_sound = pygame.mixer.Sound(r"..\music\start.wav")
        self.fire_sound = pygame.mixer.Sound(r"..\music\Gunfire.wav")
        self.bang_sound = pygame.mixer.Sound(r"..\music\bang.wav")
        self.all_sounds = [self.start_sound, self.fire_sound, self.bang_sound]
        self.set_sounds_volume([self.bang_sound], 1)
        if DEBUG:
            self.set_sounds_volume(self.all_sounds, 0)
        self.start_sound.play()

    def set_sounds_volume(self, sounds, level):
        for sd in sounds:
            sd.set_volume(level)

    def run_game(self):
        while True:
            self._check_events()
            self._check_keypressed()
            # if self.game_stats.game_active:
            #     self.ship.update()
            #     self._update_bullets()
            #     self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _update_bgmap(self):
        # 画背景
        self.screen.blit(self.background_image, (0, 0))
        # 画砖块
        for each in self.bgMap.brickGroup:
            self.screen.blit(each.image, each.rect)
        # 画石头
        for each in self.bgMap.ironGroup:
            self.screen.blit(each.image, each.rect)
        # 画home
        if self.homeSurvive:
            self.screen.blit(self.home_image, (3 + 12 * 24, 3 + 24 * 24))
        else:
            self.screen.blit(self.home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))

    def _update_tanks(self):
        # 画所有坦克
        for group in self.playerGroup, self.enemyGroup:
            for tank in group:
                if tank.check_life():
                    tank.do_time_tick()
                    if tank.check_living():
                        tank.draw_living(self.screen)
                        if tank.side == 2 and self.enemyCouldMove:
                            tank.move(self.objectGroups)
                    else:
                        tank.appearing_flash(self.screen)

    def _check_beyond_screen(self, rect):
        if rect.top < self.rect.top or rect.bottom > self.rect.bottom \
                or rect.left < self.rect.left or rect.right > self.rect.right:
            return True
        return False

    def _check_bullets_beyond_screen(self):
        for i in range(2):
            bulletGroup = self.bulletGroups[i]
            for bullet in bulletGroup.copy():
                if self._check_beyond_screen(bullet.rect):
                    bulletGroup.remove(bullet)

    def _check_bullets_collide_wall(self):
        for i in range(2):
            bulletGroup = self.bulletGroups[i]
            for bullet in bulletGroup:
                # 子弹 碰撞 brickGroup
                if pygame.sprite.spritecollide(bullet, self.bgMap.brickGroup, True, None):
                    bulletGroup.remove(bullet)
                # 子弹 碰撞 ironGroup
                if pygame.sprite.spritecollide(bullet, self.bgMap.ironGroup, bullet.strong, None):
                    bulletGroup.remove(bullet)

    def _check_bullets_collide_bullets(self):
        pygame.sprite.groupcollide(self.bulletGroups[0], self.bulletGroups[1], True, True)

    def _check_bullets_collide_tanks(self):
        for i in range(2):
            bulletGroup = self.bulletGroups[i]
            for bullet in bulletGroup:
                collisions = pygame.sprite.spritecollide(bullet, self.tankGroups[1 - i], False, None)
                if collisions:
                    bulletGroup.remove(bullet)
                for tank in collisions:
                    tank.levelDown()
                    if tank.side == 2:
                        tank.print()
                    if tank.side == 2 and tank.life == 0:
                        self.tankGroups[1 - i].remove(tank)
                        del tank
        # pygame.sprite.groupcollide(self.bulletGroups[0], self.tankGroups[1], True, True)
        # pygame.sprite.groupcollide(self.bulletGroups[1], self.tankGroups[0], True, True)

    def _update_bullets(self):
        for i in range(2):
            bulletGroup = self.bulletGroups[i]
            bulletGroup.draw(self.screen)
            for bullet in bulletGroup.copy():
                bullet.move()
        self._check_bullets_beyond_screen()
        self._check_bullets_collide_wall()
        self._check_bullets_collide_bullets()
        self._check_bullets_collide_tanks()

    def _update_food(self):
        # 最后画食物/道具
        if self.food.life:
            self.screen.blit(self.food.image, self.food.rect)
            # 我方坦克碰撞 食物/道具
            for tank in self.playerGroup:
                if pygame.sprite.collide_rect(tank, self.food):
                    self.food.life = False
                    if self.food.kind == 1:  # 吃炸弹，敌人全毁
                        for each in self.enemyGroup:
                            if pygame.sprite.spritecollide(each, self.enemyGroup, True, None):
                                self.bang_sound.play()
                    if self.food.kind == 2:  # 吃定时，敌人静止
                        self.enemyCouldMove = False
                        pygame.time.set_timer(ENEMY_COULD_MOVE_EVENT, 8000, True)
                    if self.food.kind == 3:  # 吃手枪，子弹增强，变身
                        tank.levelTo(2)
                    if self.food.kind == 4:  # 吃家盾，家得到保护，持续20秒
                        self.bgMap.draw_homewall(2)
                        pygame.time.set_timer(HOMEWALL_BRICK_EVENT, 20000, True)
                    if self.food.kind == 5:  # 吃保护帽，坦克无敌
                        tank.set_protect()
                        pass
                    if self.food.kind == 6:  # 吃五星，坦克升级
                        tank.levelUp()
                    if self.food.kind == 7:  # 吃坦克，坦克生命+1
                        tank.life += 1

    def _update_screen(self):
        self._update_bgmap()

        self._update_food()

        self._update_tanks()

        self._update_bullets()

        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出游戏
                pygame.quit()
                sys.exit()

            if event.type == MY_BULLET_COOLING_EVENT:  # 我方子弹冷却事件
                for tank in self.playerGroup:
                    tank.bulletNotCooling = True

            if event.type == ENEMY_BULLET_COOLING_EVENT:  # 敌方子弹冷却事件
                for each in self.enemyGroup:
                    each.bulletNotCooling = True
                    if not each.bullet in self.bulletGroups[1]:
                        each.shoot()

            if event.type == ENEMY_COULD_MOVE_EVENT:  # 敌方坦克静止事件
                self.enemyCouldMove = True

            if event.type == HOMEWALL_BRICK_EVENT:  # 家墙恢复成砖块20000
                self.bgMap.draw_homewall(1)

            if event.type == DELAY_EVENT:  # 延迟创建敌方坦克
                if len(self.enemyGroup) < MAX_ENEMY_NUMBER:
                    self.init_enemy_tank()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        # 显示当前各种状态，调试用
        if event.key == pygame.K_F1:
            for tank in self.playerGroup:
                tank.print()

        if event.key == pygame.K_F2:
            self.set_volume(self.all_sounds, 0)
        if event.key == pygame.K_F3:
            self.set_volume(self.all_sounds, 1)

        if event.key == pygame.K_F4:
            self.enemyCouldMove = False
            pygame.time.set_timer(ENEMY_COULD_MOVE_EVENT, 8000, True)

        if event.key == pygame.K_F5:
            self.myTank[0].set_protect()

        if event.key == pygame.K_c and pygame.KMOD_CTRL:
            pygame.quit()
            sys.exit()

        if event.key == pygame.K_e:
            self.myTank[0].levelUp()
        if event.key == pygame.K_q:
            self.myTank[0].levelDown()

        if DEBUG:
            if event.key == pygame.K_2:
                if self.myTank[0].speed == 3:
                    self.myTank[0].speed = 24
                else:
                    self.myTank[0].speed = 3
            if event.key == pygame.K_3:
                self.myTank[0].levelUp()
                self.myTank[0].levelUp()
                self.myTank[0].level = 3

        if event.key == pygame.K_1:
            self.bgMap.draw_homewall(1)
        if event.key == pygame.K_4:
            self.bgMap.draw_homewall(2)
            pygame.time.set_timer(HOMEWALL_BRICK_EVENT, 20000, True)

        if DEBUG:
            # self.myTank[0].print()
            pass

    def _check_keypressed(self):
        # 检查用户的键盘操作
        key_pressed = pygame.key.get_pressed()
        for i in range(2):
            tank = self.myTank[i]
            if tank.check_living() > 0:
                dir = -1
                if i == 0:
                    if key_pressed[pygame.K_w]:
                        dir = 0
                    if key_pressed[pygame.K_s]:
                        dir = 1
                    if key_pressed[pygame.K_a]:
                        dir = 2
                    if key_pressed[pygame.K_d]:
                        dir = 3
                else:
                    if key_pressed[pygame.K_UP]:
                        dir = 0
                    if key_pressed[pygame.K_DOWN]:
                        dir = 1
                    if key_pressed[pygame.K_LEFT]:
                        dir = 2
                    if key_pressed[pygame.K_RIGHT]:
                        dir = 3
                if not tank.moving and dir >= 0:
                    tank.change_dir(dir)
                    if tank.old_dir == tank.dir:
                        tank.moving = 8
                if tank.moving:
                    tank.moving -= 1
                    tank.move(self.objectGroups)
                if key_pressed[pygame.K_j] and i == 0 or key_pressed[pygame.K_KP0] and i == 1:
                    if not tank.bullet in self.bulletGroups[0] and tank.bulletNotCooling:
                        self.fire_sound.play()
                        tank.shoot()
                        tank.bulletNotCooling = False

    # 自定义事件（定时循环）
    def user_loop_events(self):
        # 创建敌方坦克延迟200
        pygame.time.set_timer(DELAY_EVENT, 200)
        # 创建敌方子弹延迟1000
        pygame.time.set_timer(ENEMY_BULLET_COOLING_EVENT, 1000)
        # 创建我方子弹延迟200
        pygame.time.set_timer(MY_BULLET_COOLING_EVENT, 200)


if __name__ == "__main__":
    try:
        # main()
        tank_war = TankWar()
        tank_war.run_game()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()