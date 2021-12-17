import sys
import pygame
from pygame.locals import *
from pygame.math import Vector2 as vec
from shape import Shape, Board
from random import randint

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    WIDTH, HEIGHT = 400, 850
    FPS = 5
    BOARD_SIZE = vec(WIDTH // 25, HEIGHT // 25)
    FramePerSec = pygame.time.Clock()
    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")
    random_x = randint(0, WIDTH // 25)
    fig = Shape(25)
    board = Board(BOARD_SIZE)
    while not board.can_it_be_placed(fig.get_move_position(vec(random_x, 0))):
        random_x = randint(0, WIDTH // 25)
    fig.move(vec(random_x, 0))

    gameover = False
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    while True:

        if not gameover:
            if board.can_it_be_placed(fig.get_next_down_position()):
                fig.move_down()
            else:
                board.add(fig)
                board.compact()
                fig = Shape(25)
                _random_position = vec(randint(0, int(BOARD_SIZE.x-4)), 0)
                if board.can_it_be_placed(fig.get_move_position(_random_position)):
                    fig.move(_random_position)
                else:
                    gameover = True
                    continue

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        if board.can_it_be_placed(fig.get_next_left_position()):
                            fig.move_left()
                    if event.key == pygame.K_RIGHT:
                        if board.can_it_be_placed(fig.get_next_right_position()):
                            fig.move_right()
                    if event.key == pygame.K_DOWN:
                        FPS += 15
                    if event.key == pygame.K_SPACE:
                        if board.can_it_be_placed(fig.get_rotated_position()):
                            fig.rotate_clockwise()
                    if event.key == pygame.K_n:
                        gameover = False
                        board = Board(BOARD_SIZE)
                        fig = Shape(25)
                        random_x = randint(0, WIDTH // 25)
                        while not board.can_it_be_placed(fig.get_move_position(vec(random_x, 0))):
                            random_x = randint(0, WIDTH // 25)
                        fig.move(vec(random_x, 0))
                        continue
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        FPS = 5
            displaysurface.fill((0, 0, 0))
            for y in range(1, HEIGHT // 25):
                pygame.draw.line(displaysurface, (254, 0, 0),  (0, y * 25), (WIDTH, y * 25))
            for x in range(1, WIDTH // 25):
                pygame.draw.line(displaysurface, (254, 0, 0), (x*25, 0), (x*25, HEIGHT))
            fig.draw(displaysurface)
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_n:
                        gameover = False
                        board = Board(BOARD_SIZE)
                        fig = Shape(25)
                        random_x = randint(0, WIDTH // 25)
                        while not board.can_it_be_placed(fig.get_move_position(vec(random_x, 0))):
                            random_x = randint(0, WIDTH // 25)
                        fig.move(vec(random_x, 0))
                        continue
            displaysurface.fill((0, 0, 0))
            for y in range(1, HEIGHT // 25):
                pygame.draw.line(displaysurface, (254, 0, 0),  (0, y * 25), (WIDTH, y * 25))
            for x in range(1, WIDTH // 25):
                pygame.draw.line(displaysurface, (254, 0, 0), (x*25, 0), (x*25, HEIGHT))
            fig.draw(displaysurface)
            board.draw(displaysurface)
            text_surface = myfont.render('Game Over!', False, (255, 0, 0), (0, 0, 0, 255))
            text_surface.get_rect(topleft=(10 * 25, 16 * 25))
            displaysurface.blit(text_surface, text_surface.get_rect(topleft=(5 * 25, 16 * 25)))
        board.draw(displaysurface)
        pygame.display.update()
        FramePerSec.tick(FPS)
