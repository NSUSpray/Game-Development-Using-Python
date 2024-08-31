import pygame as pg
pg.init()

filename = input('Input file name to show: ')
image = pg.image.load(filename)
size = image.get_size()
surface = pg.display.set_mode(size)
surface.blit(image, (0, 0))
pg.display.update()

input()
