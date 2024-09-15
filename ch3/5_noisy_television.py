from random import randint
import pygame as pg

pg.init()

def is_quit(event):
    return event.type == pg.QUIT \
        or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE

def rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)

running = True
clock = pg.time.Clock()
frame = pg.image.load('../ch2/television_set.png')
frame.set_colorkey((32, 32, 64))
frame_size = frame.get_size()
display = pg.display.set_mode(frame_size)

while running:
    for event in pg.event.get():
        if is_quit(event):
            running = False
            break
    display.fill((31, 31, 31))
    for y in range(120, 120 + 350, 4):
        for x in range(160, 160 + 450, 4):
            display.set_at((x, y), rand_color())
    display.blit(frame, (0, 0))
    pg.display.flip()
    clock.tick(30)
