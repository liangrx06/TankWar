# -*- coding:GBK -*-

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

MAX_ENEMY_NUMBER = 5

DIRS = ((0, -1), (0, 1), (-1, 0), (1, 0))  # �ƶ�������������


def check_rect_beyond(rect, screen_rect):
    """����Ƿ񳬳���Ļ��Χ"""
    return rect.top < screen_rect.top or rect.bottom > screen_rect.bottom \
           or rect.left < screen_rect.left or rect.right > screen_rect.right


def check_rect_inner(rect, screen_rect):
    """����Ƿ������Ļ��Χ"""
    return (screen_rect.top <= rect.top <= screen_rect.bottom
            or screen_rect.top <= rect.bottom <= screen_rect.bottom) \
           and (screen_rect.left <= rect.left <= screen_rect.right
                or screen_rect.left <= rect.right <= screen_rect.right)
