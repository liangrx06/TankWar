import pygame

DEBUG = True

RESOLUTION = (630, 630)

# 自定义事件
# 创建敌方坦克延迟200
DELAY_EVENT = pygame.constants.USEREVENT
# 创建敌方子弹延迟1000
ENEMY_BULLET_COOLING_EVENT = pygame.constants.USEREVENT + 1
# 创建我方子弹延迟200
MY_BULLET_COOLING_EVENT = pygame.constants.USEREVENT + 2
# 敌方坦克静止8000
ENEMY_COULD_MOVE_EVENT = pygame.constants.USEREVENT + 3
# 家墙恢复成砖块20000
HOMEWALL_BRICK_EVENT = pygame.constants.USEREVENT + 4

MAX_ENEMY_NUMBER = 3

DIRS = ((0,-1),(0,1),(-1,0),(1,0)) #移动方向：上下左右