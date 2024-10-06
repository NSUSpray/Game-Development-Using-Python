import math as m
import random as r
import pygame as pg

pg.init()


class NonDoublingSound:

    def __init__(self, paths):
        self.sounds = [pg.mixer.Sound(p) for p in paths]

    def play(self):
        n = len(self.sounds)
        # i = r.randint(0, m.ceil(n / 2) - 1)
        # “i” with linear PDF: argmax = 0 and argmin = n − 1 (min = 0)
        x = r.random()
        i = int((n - 1) * (1 - m.sqrt(1 - x)))
        sound = self.sounds.pop(i)
        sound.play()
        print(sound)
        self.sounds.append(sound)


pg.display.set_mode((640, 480))
clock = pg.time.Clock()
paths = [f'dog/{i}.mp3' for i in range(8)]
sound = NonDoublingSound(paths)

while True:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                exit()
            case pg.KEYUP:
                sound.play()
    clock.tick(10)
