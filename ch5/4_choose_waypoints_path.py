from dataclasses import dataclass
from itertools import product
from random import choice, shuffle
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
    def draw(self, display):
        return pg.draw.circle(
            display,
            (0, 0, 255),
            ((self.j + 0.5) * CELL_SIZE, (self.i + 0.5) * CELL_SIZE),
            CELL_SIZE / 2,
        )


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
        return super().draw(display)

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

def home_and_waypoints(mask, way_string):
    home = COLS - 1, 0
    wps = {}
    for i, j in CELLS:
        c = mask[i][j]
        if c == '$':
            home = i, j
        elif c in way_string:
            wps[c] = i, j
    waypoints = [wps[key] for key in sorted(wps.keys(), reverse=True)]
    return home, waypoints

terrain = pg.image.load('terrain.png')
mask = load_mask('terrain_with_waypoints.txt')
dist_map = init_distances(ROWS, COLS)

way_string = choice(['0345', '025', '1345', '125'])
print(way_string)
(ai, aj), waypoints = home_and_waypoints(mask, way_string)
avatar = Avatar(ai, aj)
avatar.draw(display)
target = Point(*waypoints.pop())

while True:
    if pg.QUIT in [e.type for e in pg.event.get()]: break
    if (avatar.i, avatar.j) == (target.i, target.j):
        if not waypoints: break
        dist_map = init_distances(ROWS, COLS)
        target = Point(*waypoints.pop())
        # avatar.visited.clear()
    avatar.step(mask, dist_map, target)
    display.blit(terrain, (0, 0))
    avatar.draw(display)
    pg.display.update()
    clock.tick(FPS)
