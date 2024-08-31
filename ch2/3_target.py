import pygame as pg
pg.init()

white = pg.color.Color(255, 255, 255)
black = pg.color.Color(0, 0, 0)
surface = pg.display.set_mode((400, 400))
surface.fill(pg.color.Color(127, 127, 127))
center = (200, 200)
for i in range(10, 0, -1):
	color = white if i % 2 else black
	radius = i * 10
	pg.draw.circle(surface, color, center, radius)

pg.display.update()
input()