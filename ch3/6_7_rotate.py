from math import sin, cos, pi
import pygame as pg

pg.init()
surface = pg.display.set_mode((640, 480))
rect = pg.surface.Surface((100, 50))
rect.set_colorkey((0, 0, 0))
rect.fill((0, 255, 255))

angle = 0
x = y = 240
clock = pg.time.Clock()

while True:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    pressed = pg.key.get_pressed()
    if pressed[pg.K_a]:
        angle += 10
    elif pressed[pg.K_d]:
        angle -= 10
    if pressed[pg.K_w]:
        a = angle * pi / 180
        x += 10 * cos(a)
        y -= 10 * sin(a)
    elif pressed[pg.K_s]:
        a = angle * pi / 180
        x -= 10 * cos(a)
        y += 10 * sin(a)
    surface.fill((0, 0, 0))
    rect_ = pg.transform.rotate(rect, angle)
    center_ = [wh/2 for wh in rect_.get_size()]
    surface.blit(rect_, (x - center_[0], y - center_[1]))
    pg.display.flip()
