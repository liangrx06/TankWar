import pygame

DEBUG = True

RESOLUTION = (630, 630)

# �Զ����¼�
# �����з�̹���ӳ�200
DELAY_EVENT = pygame.constants.USEREVENT
# �����з��ӵ��ӳ�1000
ENEMY_BULLET_COOLING_EVENT = pygame.constants.USEREVENT + 1
# �����ҷ��ӵ��ӳ�200
MY_BULLET_COOLING_EVENT = pygame.constants.USEREVENT + 2
# �з�̹�˾�ֹ8000
ENEMY_COULD_MOVE_EVENT = pygame.constants.USEREVENT + 3
# ��ǽ�ָ���ש��20000
HOMEWALL_BRICK_EVENT = pygame.constants.USEREVENT + 4

MAX_ENEMY_NUMBER = 3

DIRS = ((0,-1),(0,1),(-1,0),(1,0)) #�ƶ�������������