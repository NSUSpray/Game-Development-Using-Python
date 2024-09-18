from dataclasses import dataclass
from itertools import combinations
from random import randint, randrange
import pygame as pg

pg.init()
display = pg.display.set_mode((640, 480))

@dataclass
class Cube:
    pos: list[int]
    a: int
    v: list[int]
    c: tuple[int, int, int] = (0, 0, 0)
    def step(self) -> None:
        for i in range(len(self.pos)):
            self.pos[i] += self.v[i]
    def draw(self) -> None:
        pg.draw.rect(display, self.c, (*self.pos[:2], self.a, self.a))

def intersected_axis(x1, a1, x2, a2) -> bool:
    r1 = a1 / 2
    r2 = a2 / 2
    c1 = x1 + r1
    c2 = x2 + r2
    return abs(c1 - c2) < r1 + r2

def intersected(c1: Cube, c2: Cube) -> bool:
    def ia(x1, x2): return intersected_axis(x1, c1.a, x2, c2.a)
    return all(ia(*xs) for xs in zip(c1.pos, c2.pos))

def collide(c1: Cube, c2: Cube) -> None:
    for i in range(len(c1.pos)):
        c1.pos[i] -= c1.v[i]
        c2.pos[i] -= c2.v[i]
        c1.v[i], c2.v[i] = c2.v[i], c1.v[i]

clock = pg.time.Clock()
cubes = (
    Cube(
        [100, randint(150, 333), 115],
        40,
        [10, randrange(-1, 2, 2), 0],
        (255, 255, 255),
        ),
    Cube([415, 150, 115], 40, [0, 0, 0]),
    Cube([410, 191, 110], 50, [0, 0, 0]),
    Cube([405, 242, 105], 60, [0, 0, 0]),
    Cube([400, 303, 100], 70, [0, 0, 0]),
    )

while True:
    clock.tick(30)
    if pg.QUIT in [e.type for e in pg.event.get()]: exit()
    for c in cubes:
        c.step()
    for c1, c2 in combinations(cubes, 2):
        if intersected(c1, c2):
            collide(c1, c2)
    display.fill((127, 127, 127))
    for c in cubes:
        c.draw()
    pg.display.flip()
