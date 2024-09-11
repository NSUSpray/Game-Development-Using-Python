from random import randint
import pygame as pg
pg.init()

surface = pg.display.set_mode((400, 250))
surface.fill((100, 100, 100))
button_rect = 100, 100, 200, 50
default_color = 0, 0, 0
button_color = default_color
font = pg.font.Font(None, 30)
text = font.render('Change color', 1, (255, 255, 255))

def pos_in_rect(pos, rect):
    return 0 <= pos[0] - rect[0] < rect[2] and 0 <= pos[1] - rect[1] < rect[3]

def rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)

clock = pg.time.Clock()
while True:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            if pos_in_rect(event.pos, button_rect):
                match event.button:
                    case pg.BUTTON_LEFT:
                        button_color = rand_color()
                    case pg.BUTTON_MIDDLE:
                        exit()
                    case pg.BUTTON_RIGHT:
                        button_color = default_color
    surface.fill((100, 100, 100))
    pg.draw.rect(surface, button_color, button_rect)
    surface.blit(text, (130, 115))
    pg.display.update()
    clock.tick(30)
