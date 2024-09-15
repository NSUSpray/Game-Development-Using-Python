import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()

def sound(name: str) -> pg.mixer.Sound:
    return pg.mixer.Sound(f'notes/{name}.wav')

note_sounds = [sound(name) for name in 'abcdefg']
channel = pg.mixer.find_channel()

while True:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT: exit()
            case pg.KEYDOWN:
                if pg.K_a <= event.key <= pg.K_g:
                    channel.play(note_sounds[event.key - pg.K_a], -1)
            case pg.KEYUP:
                channel.stop()
    clock.tick(10)
