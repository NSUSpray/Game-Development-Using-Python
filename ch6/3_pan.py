from time import time
import pygame as pg

W, H = 120, 80
pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

def pan(s: pg.mixer.Channel, p: float) -> None:
    return s.set_volume(1 - p, p)

sound = pg.mixer.Sound('Boomerang01.mp3')
sound_len = sound.get_length()
channel = pg.mixer.find_channel()
p = 0.5
pan(channel, p)
font = pg.font.SysFont(['Arial', 'Helvetica'], 30)

t0 = time()
channel.play(sound)
while True:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT: exit()
            case pg.MOUSEMOTION:
                p = event.pos[0] / W
                pan(channel, p)
    t = time() - t0
    if t > sound_len: break
    message = f'{t:.1f}/{sound_len:.1f}'
    text = font.render(message, 1, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (0, 0))
    pg.draw.circle(screen, (255, 255, 255), (p * W, 0), 5)
    pg.display.update()
    clock.tick(10)
