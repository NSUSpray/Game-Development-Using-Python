from random import randrange
import pygame as pg

W, H = 640, 480

def rand_circle():
    r = randrange(40, 70)
    x = randrange(r, W - r)
    y = randrange(r, H - r)
    dx = randrange(1, 4) * randrange(-1, 2, 2)
    dy = randrange(5, 8) * randrange(-1, 2, 2)
    return r, x, y, dx, dy

pg.init()
display = pg.display.set_mode((W, H))
r1, x1, y1, dx1, dy1 = rand_circle()
c1 = (255, 255, 255)
c1x = (255, 0, 0)
r2, x2, y2, dx2, dy2 = rand_circle()
c2 = (0, 0, 0)
c2x = (0, 0, 255)
min_d_2 = (r1 + r2)**2
clock = pg.time.Clock()

while True:
    clock.tick(30)
    if pg.QUIT in [e.type for e in pg.event.get()]: exit()
    x1 += dx1; y1 += dy1
    x2 += dx2; y2 += dy2
    if x1 < r1 or x1 > W - r1: dx1 = -dx1
    if y1 < r1 or y1 > H - r1: dy1 = -dy1
    if x2 < r2 or x2 > W - r2: dx2 = -dx2
    if y2 < r2 or y2 > H - r2: dy2 = -dy2
    intersect = min_d_2 > (x1 - x2)**2 + (y1 - y2)**2
    display.fill((127, 127, 127))
    pg.draw.circle(display, c1x if intersect else c1, (x1, y1), r1)
    pg.draw.circle(display, c2x if intersect else c2, (x2, y2), r2)
    pg.display.flip()
