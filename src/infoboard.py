# -*- coding:GBK -*-

import pygame
import pygame.gfxdraw
import pygame.font
from pygame.sprite import Sprite

from settings import *


## COLORS ##
#                R    G    B
GRAY         = (100, 100, 100)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
BLUE         = (  0,   0, 255)
SKY_BLUE     = ( 39, 145, 251)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK   = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

pygame.init()
FONT1 = pygame.font.SysFont('SimHei', 32)
FONT2 = pygame.font.SysFont('SimHei', 72)
FONT3 = pygame.font.SysFont('SimHei', 20)


class Infoboard:
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.screen = game.screen
        self.total_screen = game.total_screen
        self.info_screen = game.info_screen

    def update(self):
        pass

    def print_gameover(self):
        self.gameover_image = pygame.image.load(r"..\image\gameover.png").convert_alpha()
        self.gameover_image = pygame.transform.scale(self.gameover_image, (250, 80))
        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_rect.center = self.screen.get_rect().center
        if self.game.time_tick // 20 % 2 == 0:
            self.screen.blit(self.gameover_image, self.gameover_rect)

    def draw_info_background(self):
        self.info_bg_image = pygame.transform.scale(self.game.background_image, INFO_RESOLUTION)
        self.info_screen.blit(self.info_bg_image, (0, 0))

    def draw_enemy_tanks(self):
        draw_text(self.info_screen, 24 * 1, 24 * 1, FONT3, 'ENEMY', PURPLE)

        image = pygame.image.load(r"..\image\enemy_1_0.png").convert_alpha()
        image = image.subsurface((0, 0), (48, 48))
        self.enemy_tank_image = pygame.transform.scale(image, (24, 24))
        rect = self.enemy_tank_image.get_rect()
        left_tanks = MAX_TOTAL_ENEMY_NUMBER - self.game.total_emeny_number + len(self.game.enemyGroup)
        for i in range(left_tanks):
            j = i // 2
            k = i % 2
            rect.x, rect.y = 24 + 24 * k, 48 + 24 * j
            self.info_screen.blit(self.enemy_tank_image, rect)

    def draw_player_tanks(self):
        self.player_tank_image = []
        for i in range(2):
            draw_text(self.info_screen, 24 + 12, 24 * (14 + 2 * i) + 12 * i, FONT3,
                  f'{i+1}P', YELLOW if i == 0 else FOREST_GREEN)

            image = pygame.image.load(r"..\image\tank_T1_0.png").convert_alpha() if i == 0 else pygame.image.load(r"..\image\tank_T2_0.png").convert_alpha()
            image = image.subsurface((0, 0), (48, 48))
            self.player_tank_image.append(pygame.transform.scale(image, (24, 24)))
            rect = self.player_tank_image[i].get_rect()
            rect.x, rect.y = 24, 24 * (15 + 2 * i) + 12 * i
            self.info_screen.blit(self.player_tank_image[i], rect)

            draw_text(self.info_screen, 24 * 2 + 12, 24 * (15 + 2 * i) + 12 * i + 2, FONT3,
                  f'{self.game.myTank[i].life}', YELLOW if i == 0 else FOREST_GREEN)

    def draw_level_info(self):
        draw_text(self.info_screen, 24 * 1, 24 * 21, FONT3, 'LEVEL', SKY_BLUE)
        draw_text(self.info_screen, 24 * 1 + 20, 24 * 22 + 4, FONT3, '1', SKY_BLUE)


def draw_text(screen, x, y, font, text, fcolor):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def draw_filled_circle(screen, x, y, r, color):
    pygame.gfxdraw.aacircle(screen, x, y, r, color)
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)
