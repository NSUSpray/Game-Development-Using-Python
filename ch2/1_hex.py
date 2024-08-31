import math
import pygame as pg
pg.init()

def hex(
        display: pg.Surface, col: pg.color.Color, h: float,
        pos: tuple[int, int]) -> None:
    x = lambda a: h * math.cos(a) + h + pos[0]
    y = lambda a: h * math.sin(a) + h + pos[1]
    for i in range(6):
        a1 = i * math.pi/3
        a2 = (i + 1) * math.pi/3
        p1, p2 = [(x(a), y(a)) for a in (a1, a2)]
        pg.draw.line(display, col, p1, p2)

display = pg.display.set_mode((640, 480))
col = pg.color.Color(255, 255, 255)
hex(display, col, 100, (-50, 50))
pg.display.update()
input()
