import pygame
from copy import deepcopy
import random
from random import choice, randrange

from pygame import draw
from shapes import figures_pos 
from colors import shape_colors

pygame.init()

LENGTH = 20
HEIGHT = 10
TILE = 38
GAME_RESOLUTION = LENGTH * TILE, HEIGHT * TILE
RESOLUTION = 1400, 520
FPS = 60


sc = pygame.display.set_mode(RESOLUTION)
game_sc = pygame.Surface(GAME_RESOLUTION)
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris game for python project by Amirmohammad khierandish")
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(LENGTH) for y in range(HEIGHT)]


figures = [[pygame.Rect(x + 1, y + HEIGHT // 2, 1 , 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(LENGTH)] for j in range(HEIGHT)]

def get_color():
     for i in range(len(shape_colors)):
         x = random.choice(shape_colors)
     return x

anim_count = 0
anim_speed = 60
anim_limit = 2000

bg = pygame.image.load('3.jpg').convert()
game_bg = pygame.image.load('1.jpg').convert()

main_font = pygame.font.Font('font/1.otf', 70)
font = pygame.font.Font('font/1.otf', 70)

# title_score = font.render('score:', True, pygame.Color('green'))

title_message = font.render('Game over , your score is :' , True , pygame.Color("black"))

title_record = font.render('High score:', True, pygame.Color('red'))

title_score = font.render('score:', True, pygame.Color('green'))

#get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

color = get_color()
next_color = get_color()

score = 0
lines =  0
#final = 0
scores = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}


def check_borders():
    if figure[i].y < 0 or figure[i].x > LENGTH - 1:    # if we put x instead y it rotate in all way
        return False
    elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:    # y > w for that problem
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

while True:
    record = get_record()
    dy, rotate = 0, False   # dx = 0 for key and rotate
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (600, 40))      # for place of grid
    game_sc.blit(game_bg, (0, 0))

# delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

# keyboard and controlling the shapes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotate = True
            elif event.key == pygame.K_RIGHT:
                anim_limit = 200
            elif event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_UP:
                dy = -1


    figure_old = deepcopy(figure)  # this is for going in up and down shapes in screen
    for i in range(len(figure)):
        figure[i].y += dy
        if not check_borders():
            figure = deepcopy(figure_old)
            break


    anim_count += anim_speed   # this is for falling shapes and running shapes in right
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(len(figure)):
            figure[i].x += 1
            if not check_borders():
                for i in range(len(figure)):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure = next_figure
                color = next_color
                next_figure = deepcopy(choice(figures))
                next_color = get_color()
                anim_limit = 2000
                break

# Rotate the shapes

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(len(figure)):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

# Check grid and line for deleting the full line

    line, lines = LENGTH - 1, 0
    for row in range(LENGTH - 1, -1, -1):
        count = 0
        for i in range(HEIGHT):
            if field[i][row]:
                count += 1
            field[i][line] = field[i][row] 
        if count < HEIGHT:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    score += scores[lines] # Updating score

# Draw the grid in main screen

    [pygame.draw.rect(game_sc, (50, 50, 50), i_rect, 1) for i_rect in grid]

# Draw figure

    for i in range(len(figure)):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

# Draw field
# This is for stay shapes in the field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)



# Draw titles

    sc.blit(title_record, (60, 50))
    sc.blit(font.render(record, True, pygame.Color('white')), (350, 50))
    show_score_at_final = score

# Game over settings

    for i in range(HEIGHT):
        if field[i][0]:
            set_record(record, score)
            field = [[0 for i in range(LENGTH)] for i in range(HEIGHT)]
            anim_count, anim_speed, anim_limit = 1, 60, 2000
            score = 0
            for i_rect in grid:
                sc.blit(title_message, (600, 120))
                sc.blit(font.render(str(show_score_at_final), True, pygame.Color('white')), (1100, 120))
                pygame.display.flip()
                clock.tick(180)

    pygame.display.flip()
    clock.tick(FPS)