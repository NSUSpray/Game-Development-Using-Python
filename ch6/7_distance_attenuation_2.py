from math import dist
import pygame as pg

W, H = 640, 480

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()

src1 = (W // 4, H // 3)
src2 = (3 * W // 4, H // 3)
listener = [W // 2, 2 * H // 3]
max_dist = dist([0, H], src2)
snd1 = pg.mixer.Sound('drum_loop.wav')
snd2 = pg.mixer.Sound('Boomerang01.mp3')

snd1.play(-1)
snd2.play(-1)
while True:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                exit()
            case pg.MOUSEMOTION:
                listener = event.pos[:]
                vol1 = 1 - dist(listener, src1) / max_dist
                vol2 = 1 - dist(listener, src2) / max_dist
                snd1.set_volume(vol1)
                snd2.set_volume(vol2)
    display.fill((0, 0, 0))
    pg.draw.circle(display, (255, 0, 0), src1, 10)
    pg.draw.circle(display, (0, 255, 0), src2, 10)
    pg.draw.circle(display, (0, 0, 255), listener, 10)
    pg.display.flip()
    clock.tick(60)
