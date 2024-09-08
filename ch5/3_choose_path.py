from dataclasses import dataclass
from itertools import product
from random import randint
import pygame as pg

W, H = 800, 600
CELL_SIZE = 20
COLS = W // CELL_SIZE
ROWS = H // CELL_SIZE
CELLS = product(range(ROWS), range(COLS))
FPS = 15.0

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()

@dataclass
class Point:
    i: int
    j: int


class Avatar(Point):

    def __init__(self, i, j, path_number):
        super().__init__(i, j)
        self.prev_i = i
        self.prev_j = j
        self.path_number = 2**path_number
        print(path_number, self.path_number)

    def draw(self, display):
        return pg.draw.circle(
            display,
            (0, 0, 255),
            ((self.j + 0.5) * CELL_SIZE, (self.i + 0.5) * CELL_SIZE),
            CELL_SIZE / 2,
        )

    def step(self, mask):
        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for di, dj in moves:
            i = self.i + di
            j = self.j + dj
            if 0 <= i < ROWS and 0 <= j < COLS \
                    and (i, j) != (self.prev_i, self.prev_j) \
                    and mask[i][j] in '0123456789ABCDEF' \
                    and int(mask[i][j], 16) & self.path_number:
                self.prev_i = self.i
                self.prev_j = self.j
                self.i = i
                self.j = j
                break


def load_mask(filename):
    mask = []
    with open(filename) as f:
        for line in f:
            row = line.strip().replace(' ', '')
            mask.append(list(row))
    return mask

def home(mask):
    for i, j in CELLS:
        if mask[i][j] == '$':
            return i, j
    return COLS - 1, 0

terrain = pg.image.load('terrain.png')
mask = load_mask('terrain_with_paths.txt')

ai, aj = home(mask)
avatar = Avatar(ai, aj, randint(0, 3))
avatar.draw(display)

while True:
    for e in pg.event.get():
        match e.type:
            case pg.QUIT: exit()
            case pg.KEYDOWN:
                avatar = Avatar(ai, aj, randint(0, 3))
    if mask[avatar.i][avatar.j] == 'F': break
    avatar.step(mask)
    display.blit(terrain, (0, 0))
    avatar.draw(display)
    pg.display.update()
    clock.tick(FPS)
