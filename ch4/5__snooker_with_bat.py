from dataclasses import dataclass
from itertools import combinations
from math import atan2, cos, hypot, inf, sin, sqrt
from typing import Literal

import pygame as pg


WIDTH = 640
HEIGHT = 480
SCREEN_SIZE = WIDTH, HEIGHT
FPS = 60.0
DT = 1 / FPS
DECELERATION = 0.85  # per second
BAT_LEN = 200

pg.init()
display = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()


@dataclass
class Wall:
    direction: Literal['-', '|']
    pos: float
    def __hash__(self) -> int: return id(self)


class Ball:

    r = 10.0

    def __init__(
            self,
            pos: list[float],
            vel: list[float],
            color: tuple[int, int, int]=(255, 0, 0)
            ) -> None:
        self.pos = pos
        self.vel = vel  # pixels per second
        self._color = color

    def __repr__(self) -> str:
        return (f'Ball(pos=[{round(self.pos[0])}, {round(self.pos[1])}],'
                f' vel=[{round(self.vel[0])}, {round(self.vel[1])}])')

    def step(self, dt: float) -> None:
        self.pos = [x + v*dt for x, v in zip(self.pos, self.vel)]
        self.vel = [v * DECELERATION**dt for v in self.vel]
        if abs(sum([v*v for v in self.vel])) < self.r*2:
            self.vel = [0.0, 0.0]

    def draw(self) -> pg.Rect:
        return pg.draw.circle(display, self._color, self.pos, self.r)


class Bat:

    def __init__(self, cue: Ball):
        self._cue = cue
        self.vel = 0.0

    @property
    def pos(self) -> list[float]:
        bat_pos_rel = [
            bx - cx for bx, cx in zip(pg.mouse.get_pos(), self._cue.pos)
            ]
        bat_pos_len = hypot(*bat_pos_rel)
        return [x / bat_pos_len for x in bat_pos_rel]


Body = Wall | Ball
Pair = tuple[Body, Body]


def arrange_balls() -> tuple[set[Ball], Ball]:
    balls = set()
    for i in range(6):
        x = 3 * WIDTH / 4 + i * (Ball.r + 0.1) * sqrt(3)
        for j in range(i + 1):
            y = HEIGHT / 2 - i * (Ball.r + 0.1) + j * (Ball.r + 0.1)*2
            ball = Ball([x, y], [0, 0])
            balls.add(ball)
    cue = Ball([WIDTH / 4, HEIGHT / 2], [0, 0], (255, 255, 255))
    balls.add(cue)
    return balls, cue


def collision_time(pair: Pair) -> float:
    body, ball = sorted(pair, key=lambda b: type(b) is Ball)
    assert type(ball) is Ball
    if type(body) is Wall:
        wall = body
        ax = { '|': 0, '-': 1 }[wall.direction]
        padding = ball.r * (2*(ball.vel[ax] < 0) - 1)
        try:
            t = (wall.pos + padding - ball.pos[ax]) / ball.vel[ax]
        except ZeroDivisionError:
            return inf
        if t > 0: return t
    elif type(body) is Ball:
        ball2 = body
        x1, y1 = ball.pos
        x2, y2 = ball2.pos
        dx, dy = x2 - x1, y2 - y1
        Vx, Vy = [v1 - v2 for v1, v2 in zip(ball.vel, ball2.vel)]
        dx_dot_V = dx*Vx + dy*Vy
        if dx_dot_V < 0: return inf
        V2 = Vx*Vx + Vy*Vy
        diam2 = 4 * Ball.r * Ball.r
        A, B, C = Vy, -Vx, Vx*y1 - Vy*x1
        try:
            d2 = (A*x2 + B*y2 + C)**2 / V2
        except ZeroDivisionError:
            return inf
        if d2 > diam2: return inf
        try:
            sqrtD = sqrt(diam2*V2 - (Vx*dy - Vy*dx)**2)
            t1 = (dx_dot_V - sqrtD) / V2
            t2 = (dx_dot_V + sqrtD) / V2
            return min(t for t in (t1, t2) if t > 0)
        except (ValueError, ZeroDivisionError):
            return inf
    return inf


def rotate(v1: list[float], theta: float) -> list[float]:
    s, c = sin(theta), cos(theta)
    return [v1[0] * c - v1[1] * s, v1[0] * s + v1[1] * c]


def redirect(pair: Pair) -> Pair:
    body, ball = sorted(pair, key=lambda b: type(b) is Ball)
    assert type(ball) is Ball
    if type(body) is Wall:
        wall = body
        ax = { '|': 0, '-': 1 }[wall.direction]
        ball.vel[ax] *= -1
    elif type(body) is Ball:
        ball2 = body
        dx, dy = [x2 - x1 for x1, x2 in zip(ball.pos, ball2.pos) ]
        theta = atan2(dy, dx)
        v1 = rotate(ball.vel, -theta)
        u1 = rotate(ball2.vel, -theta)
        v2 = [u1[0], v1[1]]
        u2 = [v1[0], u1[1]]
        ball.vel = rotate(v2, theta)
        ball2.vel = rotate(u2, theta)
    return pair


def dict_min(d: dict[Pair, float]) -> tuple[Pair, float]:
    key = min(d, key=d.get)
    return key, d[key]


def hit_bat(bat: Bat, cue: Ball) -> None:
    cue.vel = [- 300 * x * bat.vel for x in bat.pos]
    bat.vel = 0


walls = {
    Wall('|', 0), Wall('|', WIDTH),
    Wall('-', 0), Wall('-', HEIGHT),
    }
balls, cue = arrange_balls()
bodies = walls | balls
pairs = set(combinations(bodies, 2)) - set(combinations(walls, 2))
collision_times = dict.fromkeys(pairs, inf)
bat = Bat(cue)

while True:
    for e in pg.event.get():
        match e.type:
            case pg.QUIT: exit()
            case pg.MOUSEBUTTONUP:
                if any(cue.vel): break
                hit_bat(bat, cue)
            case pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    cue.vel = [0, 0]
    if not any(cue.vel) and pg.mouse.get_pressed()[0]:
        bat.vel += DT
    dt = DT
    while True:
        collision_times = { p: collision_time(p) for p in pairs }
        colliding_pair, min_coll_t = dict_min(collision_times)
        if min_coll_t > dt: break
        for ball in balls: ball.step(min_coll_t)
        dt -= min_coll_t
        redirect(colliding_pair)
    for ball in balls: ball.step(dt)
    display.fill((0, 127, 0))
    if bat.vel:
        dist = Ball.r + 2*Ball.r * sqrt(bat.vel)
        start_pos = [cx + bx * dist for cx, bx in zip(cue.pos, bat.pos)]
        end_pos = [cx + bx * (dist + BAT_LEN) for cx, bx in zip(cue.pos, bat.pos)]
        pg.draw.line(display, (255, 255, 127), start_pos, end_pos, 5)
    for ball in balls: ball.draw()
    pg.display.update()
    clock.tick(FPS)
