from math import dist
import pygame as pg

W, H = 640, 480

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()

source = (W // 2, H // 3)
listener = [W // 2, 2 * H // 3]
max_dist = dist([0, H], source)
sound = pg.mixer.Sound('drum_loop.wav')

sound.play(-1)
while True:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                exit()
            case pg.MOUSEMOTION:
                listener = event.pos[:]
                volume = 1 - dist(listener, source) / max_dist
                sound.set_volume(volume)
    display.fill((0, 0, 0))
    pg.draw.circle(display, (255, 0, 0), source, 10)
    pg.draw.circle(display, (0, 0, 255), listener, 10)
    pg.display.flip()
    clock.tick(60)
