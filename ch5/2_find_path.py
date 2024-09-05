from dataclasses import dataclass
from itertools import product
from random import shuffle
from math import hypot, inf
import pygame as pg

W, H = 800, 600
CELL_SIZE = 20
COLS = W // CELL_SIZE
ROWS = H // CELL_SIZE
CELLS = product(range(ROWS), range(COLS))
FPS = 5.0

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()

@dataclass
class Point:
    i: int
    j: int


class Avatar(Point):

    path = []
    visited = []

    def draw(self, display):
        for i, j in self.visited:
            pg.draw.circle(
                display,
                (0, 0, 255),
                ((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),
                CELL_SIZE / 6,
            )
        return pg.draw.circle(
            display,
            (0, 0, 255),
            ((self.j + 0.5) * CELL_SIZE, (self.i + 0.5) * CELL_SIZE),
            CELL_SIZE / 2,
        )

    def step(self, mask, dist_map, target):
        if dist_map[self.i][self.j] is None:
            dist_map[self.i][self.j] = \
                    hypot(target.i - self.i, target.j - self.j)
            self.visited.append((self.i, self.j))
        dist = dist_map[self.i][self.j]
        #moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        shuffle(moves)
        min_ddist = inf
        move = None
        for di, dj in moves:
            i = self.i + di
            j = self.j + dj
            if not (0 <= i < ROWS and 0 <= j < COLS):
                continue
            if dist_map[i][j] is None:
                dist_map[i][j] = hypot(target.i - i, target.j - j)
            if (i, j) not in self.visited and mask[i][j] not in '#%':
                #factor = 1.0
                factor = 1.0 if di == 0 or dj == 0 else 0.707  # 1/sqrt(2)
                if (dist_map[i][j] - dist) * factor < min_ddist:
                    min_ddist = (dist_map[i][j] - dist) * factor
                    move = i, j
        if move:
            self.i, self.j = move
            self.path.append(move)
            self.visited.append(move)
        else:
            self.i, self.j = self.path.pop()


def load_mask(filename):
    mask = []
    with open(filename) as f:
        for line in f:
            row = line.strip().replace(' ', '')
            mask.append(list(row))
    return mask

def init_distances(rows, cols):
    return [[None for j in range(cols)] for i in range(rows)]

def home_and_target(mask):
    home = COLS - 1, 0
    target = 0, ROWS - 1
    for i, j in CELLS:
        match mask[i][j]:
            case '$':
                home = i, j
            case 'O':
                target = i, j
    return home, target

terrain = pg.image.load('terrain.png')
mask = load_mask('terrain.txt')
dist_map = init_distances(ROWS, COLS)

(ai, aj), (ti, tj) = home_and_target(mask)
avatar = Avatar(ai, aj)
avatar.draw(display)
target = Point(ti, tj)

while True:
    if pg.QUIT in [e.type for e in pg.event.get()]: break
    if mask[avatar.i][avatar.j] in '@O': break
    avatar.step(mask, dist_map, target)
    display.blit(terrain, (0, 0))
    avatar.draw(display)
    pg.display.update()
    clock.tick(FPS)
