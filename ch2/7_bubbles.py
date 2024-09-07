from random import randint

import pygame as pg

pg.init()

def is_quit(event):
    return event.type == pg.QUIT \
        or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE

WIDTH = 640
HEIGHT = 480
FPS = 60
BLACK = pg.color.Color(0, 0, 0)
WHITE = pg.color.Color(255, 255, 255)
SPEED = 1
surface = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
bubbles = []

running = True
while running:
    for event in pg.event.get():
        if is_quit(event):
            running = False
            break
    surface.fill(BLACK)
    bubbles.append([randint(0, WIDTH - 1), HEIGHT])
    for i in range(len(bubbles)):
        y = bubbles[i][1]
        bubbles[i][1] = y - SPEED
        r = (HEIGHT - y) / 20
        pg.draw.circle(surface, WHITE, bubbles[i], r, 1)
    bubbles = [b for b in bubbles if b[1] > 0]
    pg.display.flip()
    clock.tick(FPS)
