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

MAX_ENEMY_NUMBER = 5

DIRS = ((0,-1),(0,1),(-1,0),(1,0)) #移动方向：上下左右


# 检查是否超出屏幕范围
def check_rect_beyond(rect, screen_rect):
    return rect.top < screen_rect.top or rect.bottom > screen_rect.bottom \
            or rect.left < screen_rect.left or rect.right > screen_rect.right

# 检查是否进入屏幕范围
def check_rect_inner(rect, screen_rect):
    return (screen_rect.top <= rect.top <= screen_rect.bottom \
            or screen_rect.top <= rect.bottom <= screen_rect.bottom) \
            and (screen_rect.left <= rect.left <= screen_rect.right \
            or screen_rect.left <= rect.right <= screen_rect.right)