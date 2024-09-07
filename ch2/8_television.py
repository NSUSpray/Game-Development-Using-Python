import pygame as pg

pg.init()

def is_quit(event):
    return event.type == pg.QUIT \
        or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE

running = True
clock = pg.time.Clock()
frame = pg.image.load('television_set.png')
frame.set_colorkey((32, 32, 64))
frame_size = frame.get_size()
display = pg.display.set_mode(frame_size)
noise = [f'tv_noise/{i}.png' for i in range(13)]
noise = [pg.image.load(n) for n in noise]
noise = [pg.transform.scale_by(n, 1.3) for n in noise]

i = 0
while running:
    for event in pg.event.get():
        if is_quit(event):
            running = False
            break
    display.blit(noise[i], (160, 120))
    i = (i + 1) % 13
    display.blit(frame, (0, 0))
    pg.display.flip()
    clock.tick(30)
