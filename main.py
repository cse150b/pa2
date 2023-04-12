# NOTE: Do not modify.
from __future__ import absolute_import, division, print_function
import sys, time, math, random, os, argparse
from game import Game
from ai import AI
from test import test, test_ec

random.seed(0)

MAXC = 255
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (244, 67, 54)
PINK = (234, 30, 99)
PURPLE = (156, 39, 176)
DEEP_PURPLE = (103, 58, 183)
BLUE = (33, 150, 243)
TEAL = (0, 150, 136)
L_GREEN = (139, 195, 74)
GREEN = (60, 175, 80)
ORANGE = (255, 152, 0)
DEEP_ORANGE = (255, 87, 34)
BROWN = (121, 85, 72)
COLORS = { 0:WHITE, 2:RED, 4:PINK, 8:PURPLE, 16:DEEP_PURPLE,
               32:BLUE, 64:TEAL, 128:L_GREEN, 256:GREEN,
               512:ORANGE, 1024: DEEP_ORANGE, 2048:BROWN, 
               4096:DEEP_PURPLE, 8192:DEEP_ORANGE, 16384:BROWN, 32768:TEAL}

BOARD_SIZE_PX = 400
BOARD_Y_OFFSET_PX = 50
TEXT_X_OFFSET_PX = 10
TEXT_Y_OFFSET_PX = 10
SCORE_LABEL_POS = (10, 10)
EC_LABEL_POS = (350, 10)


PADDING = 5

MAX_CORD = 13

class GameRunner:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self.surface = pygame.display.set_mode((BOARD_SIZE_PX, BOARD_SIZE_PX + BOARD_Y_OFFSET_PX), 0, 32)
        self.myfont = pygame.font.SysFont("arial", 20)
        self.scorefont = pygame.font.SysFont("arial", 20)

        self.grayscale = False
        self.game = Game()
        self.auto = False
        self.ec = False

    def loop(self):
        while True:
            game_over = self.game.game_over()
            if game_over:
                self.auto = False

            direction = None
            for event in pygame.event.get():
                if not game_over:
                    if event.type == KEYDOWN:
                        if self.is_arrow(event.key):
                            direction = ROTATIONS[event.key]
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.auto = not self.auto
                    if event.key == K_e:
                        self.ec = not self.ec
                    if event.key == pygame.K_r:
                        self.game.set_state()
                        self.auto = False
                    if 50 < event.key and 56 > event.key:
                        self.game.board_size = event.key - 48
                        self.game.set_state()
                        self.auto = False
                    if event.key == pygame.K_s:
                        self.game.save_state()
                    elif event.key == pygame.K_l:
                        self.game.load_state()
                    elif event.key == pygame.K_u:
                        self.game.undo()
                    elif event.key == pygame.K_g:
                        self.grayscale = not self.grayscale

            if self.auto and not game_over:
                ai = AI(self.game.current_state())
                if not self.ec:
                    direction = ai.compute_decision() 
                else:
                    direction = ai.compute_decision_ec() 

            if direction != None:
                self.game.move_and_place(direction)

            self.print_matrix()
            if game_over:
                self.print_game_over()
            pygame.display.update()
        
    def print_matrix(self):
        tile_size = BOARD_SIZE_PX/self.game.board_size
        self.surface.fill(WHITE)
        for i in range(0, self.game.board_size):
            for j in range(0, self.game.board_size):
                tile_count = self.game.tile_matrix[i][j]
                ul_x_px = i*tile_size
                ul_y_px = j*tile_size + BOARD_Y_OFFSET_PX
                color = None
                if self.grayscale:
                    color_order = min(math.log(tile_count, 2), MAX_CORD) if tile_count > 0 else 0
                    color = MAXC - ((color_order / float(MAX_CORD)) * MAXC)
                    color = [color] * 3
                else: 
                    color = COLORS[tile_count]
                pygame.draw.rect(self.surface, color,
                    (ul_x_px, ul_y_px, tile_size, tile_size))
                pygame.draw.rect(self.surface, BLACK,
                    (ul_x_px, ul_y_px, tile_size, tile_size), 2)
                tile_lbl = self.myfont.render(str(tile_count), 1, BLACK)
                score_lbl = self.getScoreLabel()

                tile_lbl_x = ul_x_px + TEXT_X_OFFSET_PX
                tile_lbl_y = ul_y_px + TEXT_Y_OFFSET_PX
                tile_lbl_pos = (tile_lbl_x, tile_lbl_y)
                self.draw_label_hl(tile_lbl_pos, tile_lbl, 2, [230] * 3, 1, False)
                self.surface.blit(tile_lbl, tile_lbl_pos)

                self.surface.blit(score_lbl, SCORE_LABEL_POS)

                if self.ec:
                    ec_lbl = self.scorefont.render("[EC]", 1, BLACK, WHITE)
                    self.surface.blit(ec_lbl, EC_LABEL_POS)

    def getScoreLabel(self):
        return self.scorefont.render("Score: {}".format(self.game.score), 1, BLACK, WHITE)

    def draw_label_hl(self, pos, label, padding=PADDING, bg=WHITE, wd=2, border=True):
        specs = [(bg, 0)]
        if border:
            specs += [(BLACK, wd)]
        for color, width in specs:
            pygame.draw.rect(self.surface, color,
                (pos[0] - padding, pos[1] - padding, label.get_width() + padding * 2, label.get_height() + padding * 2), width)

    def print_game_over(self):
        game_over_lbl = self.scorefont.render("Game Over!", 1, BLACK, WHITE)
        score_lbl = self.getScoreLabel()
        restart_lbl = self.myfont.render("Press r to restart!", 1, BLACK, WHITE)

        for lbl, pos in [ (game_over_lbl, (50, 100)), (score_lbl, (50, 200)), (restart_lbl, (50, 300))]:
            self.draw_label_hl(pos, lbl)
            self.surface.blit(lbl, pos)

    def is_arrow(self, k):
        return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

parser = argparse.ArgumentParser(description='2048.')
parser.add_argument('--test', '-t', dest="test", type=int, default=0, help='0: initializes game, 1: autograde')
args = parser.parse_args()

if __name__ == '__main__':
    if args.test == 1:
        test()
    elif args.test == 2:
        test_ec()
    else:
        import pygame
        from pygame.locals import *
        ROTATIONS = {pygame.K_UP: 0, pygame.K_DOWN: 2, pygame.K_LEFT: 1, pygame.K_RIGHT: 3}
        game = GameRunner()
        game.loop()
