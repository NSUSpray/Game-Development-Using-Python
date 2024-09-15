from time import time
import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()

sound = pg.mixer.Sound('Boomerang01.mp3')
sound_len = sound.get_length()
font = pg.font.SysFont(['Arial', 'Helvetica'], 30)

t0 = time()
sound.play()
while True:
	t = time() - t0
	if t > sound_len: break
	text = font.render(f'{t:.1f}/{sound_len:.1f} s', 1, [255]*3)
	screen.fill([0]*3)
	screen.blit(text, (0, 0))
	pg.display.update()
	clock.tick(25)
