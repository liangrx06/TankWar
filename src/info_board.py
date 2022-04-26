import pygame
import pygame.gfxdraw
import pygame.font
from pygame.sprite import Sprite

from settings import *


class ChessBoard:
    def __init__(self, game):
        super().__init__()
        self.stats = game.stats
        self.screen = game.screen
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

    def update(self):
        pass

    def print_win_msg(self):
        fwidth, fheight = FONT2.size('黑方获胜')
        winner_name = '黑方' if self.stats.winner == 1 else '白方'
        draw_text(self.screen, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, FONT2, winner_name + '获胜', RED_COLOR)

    def draw_chess_board(self):
        # 画棋盘网格线外的边框
        pygame.draw.rect(self.screen, BLACK_COLOR, (OUTER_WIDTH, OUTER_WIDTH, BORDER_LENGTH, BORDER_LENGTH),
                         BORDER_WIDTH)

        # 画网格线
        for j in range(LINE_POINTS):
            pygame.draw.line(self.screen, BLACK_COLOR,
                             (START_X + WIDTH * j, START_X),
                             (START_X + WIDTH * j, START_X + WIDTH * (LINE_POINTS - 1)),
                             1)
        for i in range(LINE_POINTS):
            pygame.draw.line(self.screen, BLACK_COLOR,
                             (START_Y, START_Y + WIDTH * i),
                             (START_Y + WIDTH * (LINE_POINTS - 1), START_Y + WIDTH * i),
                             1)

        # 画星位和天元
        for i in (3, 9, 15):
            for j in (3, 9, 15):
                if i == j == 9:
                    radius = 5
                else:
                    radius = 3
                draw_filled_circle(self.screen, START_X + WIDTH * i, START_Y + WIDTH * j, radius, BLACK_COLOR)

    def draw_left_info(self):
        draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2, RADIUS2, BLACK_COLOR)
        draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, START_X + RADIUS2 * 4, RADIUS2, WHITE_COLOR)

        draw_text(self.screen, RIGHT_INFO_POS_X, START_X + 3, FONT1, '玩家', BLUE_COLOR)
        draw_text(self.screen, RIGHT_INFO_POS_X, START_X + RADIUS2 * 3 + 3, FONT1, '电脑', BLUE_COLOR)

        draw_text(self.screen, SCREEN_HEIGHT, SCREEN_HEIGHT - RADIUS2 * 8, FONT1, '战况：', BLUE_COLOR)
        draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - int(RADIUS2 * 4.5), RADIUS2, BLACK_COLOR)
        draw_filled_circle(self.screen, SCREEN_HEIGHT + RADIUS2, SCREEN_HEIGHT - RADIUS2 * 2, RADIUS2, WHITE_COLOR)
        draw_text(self.screen, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(RADIUS2 * 5.5) + 3, FONT1, f'{self.stats.scores[0]} 胜', BLUE_COLOR)
        draw_text(self.screen, RIGHT_INFO_POS_X, SCREEN_HEIGHT - RADIUS2 * 3 + 3, FONT1, f'{self.stats.scores[1]} 胜', BLUE_COLOR)


class Chess(Sprite):
    def __init__(self, ai_game, side, point):
        super().__init__()
        self.screen = ai_game.screen

        self.set_side(side)
        self.set_point(point)

    def set_side(self, side):
        self.side = side
        self.color = BLACK_COLOR if self.side == 1 else WHITE_COLOR

    def set_point(self, point):
        self.i, self.j = point

    def update(self):
        pass

    def draw(self):
        if self.side == 0:
            return
        draw_filled_circle(self.screen, START_X + WIDTH * self.i, START_Y + WIDTH * self.j, RADIUS, self.color)


def draw_text(screen, x, y, font, text, fcolor):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def draw_filled_circle(screen, x, y, r, color):
    pygame.gfxdraw.aacircle(screen, x, y, r, color)
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)
