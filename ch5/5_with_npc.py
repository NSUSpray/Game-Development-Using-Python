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

MOVES = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()


Mask = list[list[str]]
DistMap = list[list[float | None]]


@dataclass
class Point:

    i: int
    j: int
    r = 1 / 6
    c = (127, 127, 127)

    def draw(self, display: pg.Surface) -> pg.Rect:
        cx = (self.j + 0.5) * CELL_SIZE
        cy = (self.i + 0.5) * CELL_SIZE
        r = self.r * CELL_SIZE
        return pg.draw.circle(display, self.c, (cx, cy), r)


class Character(Point):

    r = 1 / 2

    def step(self, target: Point, *args, **kwargs) -> None:
        self.i, self.j = target.i, target.j


class Avatar(Character):

    c = (0, 0, 255)
    path: list[Point] = []
    visited: list[Point] = []

    def draw(self, display: pg.Surface) -> pg.Rect:
        for point in self.visited:
            point.draw(display)
        return super().draw(display)

    def step(self, target: Point, mask: Mask, dist_map: DistMap) -> None:
        if dist_map[self.i][self.j] is None:
            dist_map[self.i][self.j] = \
                    hypot(target.i - self.i, target.j - self.j)
            self.visited.append(Point(self.i, self.j))
        dist = dist_map[self.i][self.j]
        moves = MOVES[:]
        shuffle(moves)
        min_ddist = inf
        move: Point | None = None
        for di, dj in moves:
            i = self.i + di
            j = self.j + dj
            if not (0 <= i < ROWS and 0 <= j < COLS):
                continue
            if dist_map[i][j] is None:
                dist_map[i][j] = hypot(target.i - i, target.j - j)
            if Point(i, j) not in self.visited and mask[i][j] not in '#%':
                factor = 1.0 if di == 0 or dj == 0 else 0.707  # 1/sqrt(2)
                if (dist_map[i][j] - dist) * factor < min_ddist:
                    min_ddist = (dist_map[i][j] - dist) * factor
                    move = Point(i, j)
        if move:
            super().step(move)
            self.path.append(move)
            self.visited.append(move)
        else:
            super().step(self.path.pop())


class Enemy(Character):

    c = (255, 0, 0)

    def is_visible(self, target: Point, mask: Mask) -> bool:
        r = lambda *i: range(min(i), max(i) + 1)
        ti, tj = target.i, target.j
        cells = product(r(self.i, ti), r(self.j, tj))
        dot = tj * self.i - ti * self.j
        l2 = (self.i - ti)**2 + (self.j - tj)**2
        for i, j in cells:
            if mask[i][j] not in '#@': continue
            dist2 = ((ti - self.i) * j - (tj - self.j) * i + dot)**2 / l2
            if dist2 < self.r * self.r: return False
        return True

    def step(self, target: Point, mask: Mask) -> None:
        moves = MOVES[:]
        shuffle(moves)
        min_ddist = inf
        move: Point | None = None
        for di, dj in moves:
            i = self.i + di
            j = self.j + dj
            if not (0 <= i < ROWS and 0 <= j < COLS):
                continue
            if mask[i][j] not in '#%':
                dist = hypot(target.i - i, target.j - j)
                factor = 1.0 if di == 0 or dj == 0 else 0.707  # 1/sqrt(2)
                if dist * factor < min_ddist:
                    min_ddist = dist * factor
                    move = Point(i, j)
        if move:
            super().step(move)


def load_mask(filename: str) -> Mask:
    mask: Mask = []
    with open(filename) as f:
        for line in f:
            row = line.strip().replace(' ', '')
            mask.append(list(row))
    return mask


def init_distances(rows: int, cols: int) -> DistMap:
    return [[None for _ in range(cols)] for _ in range(rows)]


def objects(mask: Mask, way_string: str) -> (
        tuple[tuple[int, int], list[tuple[int, int]], tuple[int, int]]
        ):
    home = COLS - 1, ROWS - 1
    wps: dict[str, tuple[int, int]] = {}
    enemy = 0, 0
    for i, j in CELLS:
        c = mask[i][j]
        if c == '$':
            home = i, j
        elif c in way_string:
            wps[c] = i, j
        elif c == 'M':
            enemy = i, j
    waypoints = [wps[key] for key in sorted(wps.keys(), reverse=True)]
    return home, waypoints, enemy


terrain = pg.image.load('terrain.png')
mask = load_mask('terrain_with_waypoints.txt')
dist_map = init_distances(ROWS, COLS)

way_string = choice(['0345', '025', '1345', '125'])
print('waypoints:', way_string)
(ai, aj), waypoints, (ei, ej) = objects(mask, way_string)
avatar = Avatar(ai, aj)
avatar.draw(display)
target = Point(*waypoints.pop())
enemy = Enemy(ei, ej)


while True:
    if pg.QUIT in [e.type for e in pg.event.get()]: break

    if (avatar.i, avatar.j) == (target.i, target.j):
        if not waypoints:
            print('blue wins')
            break
        dist_map = init_distances(ROWS, COLS)
        target = Point(*waypoints.pop())
    elif abs(enemy.i - avatar.i) <= 1 and abs(enemy.j - avatar.j) <= 1:
        print('red wins')
        break
        
    avatar.step(target, mask, dist_map)
    if enemy.is_visible(avatar, mask):
        enemy.step(target, mask)

    display.blit(terrain, (0, 0))
    avatar.draw(display)
    enemy.draw(display)
    pg.display.update()

    clock.tick(FPS)
