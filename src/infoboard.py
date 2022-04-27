# -*- coding:GBK -*-

import pygame
import pygame.gfxdraw
import pygame.font
from pygame.sprite import Sprite

from settings import *


BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)

pygame.init()
FONT1 = pygame.font.SysFont('SimHei', 32)
FONT2 = pygame.font.SysFont('SimHei', 72)


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

    def print_info_background(self):
        self.info_bg_image = pygame.transform.scale(self.game.background_image, INFO_RESOLUTION)
        self.info_screen.blit(self.info_bg_image, (0, 0))

    def print_enemy_tanks(self):
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

    # def draw_chess_board(self):
    #     # 画棋盘网格线外的边框
    #     pygame.draw.rect(self.screen, BLACK_COLOR, (OUTER_WIDTH, OUTER_WIDTH, BORDER_LENGTH, BORDER_LENGTH),
    #                      BORDER_WIDTH)
    #
    #     # 画网格线
    #     for j in range(LINE_POINTS):
    #         pygame.draw.line(self.screen, BLACK_COLOR,
    #                          (START_X + WIDTH * j, START_X),
    #                          (START_X + WIDTH * j, START_X + WIDTH * (LINE_POINTS - 1)),
    #                          1)
    #     for i in range(LINE_POINTS):
    #         pygame.draw.line(self.screen, BLACK_COLOR,
    #                          (START_Y, START_Y + WIDTH * i),
    #                          (START_Y + WIDTH * (LINE_POINTS - 1), START_Y + WIDTH * i),
    #                          1)
    #
    #     # 画星位和天元
    #     for i in (3, 9, 15):
    #         for j in (3, 9, 15):
    #             if i == j == 9:
    #                 radius = 5
    #             else:
    #                 radius = 3
    #             draw_filled_circle(self.screen, START_X + WIDTH * i, START_Y + WIDTH * j, radius, BLACK_COLOR)

    # def draw_left_info(self):
    #     draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2, RADIUS2, BLACK_COLOR)
    #     draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2 * 4, RADIUS2, WHITE_COLOR)
    #
    #     draw_text(self.screen, RIGHT_INFO_POS_X, START_X + 3, FONT1, '玩家', BLUE_COLOR)
    #     draw_text(self.screen, RIGHT_INFO_POS_X, START_X + RADIUS2 * 3 + 3, FONT1, '电脑', BLUE_COLOR)
    #
    #     draw_text(self.screen, SCREEN_HEIGHT, SCREEN_HEIGHT - RADIUS2 * 8, FONT1, '战况：', BLUE_COLOR)
    #     draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - int(RADIUS2 * 4.5), RADIUS2, BLACK_COLOR)
    #     draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - RADIUS2 * 2, RADIUS2, WHITE_COLOR)
    #     draw_text(self.screen, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(RADIUS2 * 5.5) + 3, FONT1, f'{self.stats.scores[0]} 胜', BLUE_COLOR)
    #     draw_text(self.screen, RIGHT_INFO_POS_X, SCREEN_HEIGHT - RADIUS2 * 3 + 3, FONT1, f'{self.stats.scores[1]} 胜', BLUE_COLOR)


# class Chess(Sprite):
#     def __init__(self, ai_game, side, point):
#         super().__init__()
#         self.screen = ai_game.screen
#
#         self.set_side(side)
#         self.set_point(point)
#
#     def set_side(self, side):
#         self.side = side
#         self.color = BLACK_COLOR if self.side == 1 else WHITE_COLOR
#
#     def set_point(self, point):
#         self.i, self.j = point
#
#     def update(self):
#         pass
#
#     def draw(self):
#         if self.side == 0:
#             return
#         draw_filled_circle(self.screen, START_X + WIDTH * self.i, START_Y + WIDTH * self.j, RADIUS, self.color)


def draw_text(screen, x, y, font, text, fcolor):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def draw_filled_circle(screen, x, y, r, color):
    pygame.gfxdraw.aacircle(screen, x, y, r, color)
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)
