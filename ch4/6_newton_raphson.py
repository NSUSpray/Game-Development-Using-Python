from math import cos, pi, sin
import pygame as pg

FPS = 60.0
DT = 1 / FPS
BAT_LEN = 240  # bat length
R = 20

pg.init()
display = pg.display.set_mode((640, 480))
clock = pg.time.Clock()

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

def distance(x, y, φ):
    A, B, C = sin(φ), -cos(φ), 0
    return A * x + B * y + C

def will_collide(x, y, vx, vy, φ, ω, dt):
    in_bounds_1 = x*x + y*y < (BAT_LEN + R) ** 2
    d1 = distance(x, y, φ)
    x += vx * dt
    y += vy * dt
    φ += ω * dt
    in_bounds_2 = x*x + y*y < (BAT_LEN + R) ** 2
    d2 = distance(x, y, φ)
    if not in_bounds_1 and not in_bounds_2:
        return False
    # return d1 * d2 < 0  # point
    return abs(d1) > R and (abs(d2) < R or d1 * d2 < 0)  # circle

def newton_raphson(t0, f, df, args, tol=1e-6, max_iter=100):
    t = t0
    for _ in range(max_iter):
        ft = f(t, *args)
        dft = df(t, *args)
        t_new = t - ft / dft
        if abs(t_new - t) < tol:
            return t_new
        t = t_new
    return t

def display_all(x: float, y: float, φ: float) -> None:
    display.fill((0, 127, 0))
    # display.set_at([round(x), round(y)], (255, 255, 255))
    pg.draw.circle(display, (255, 255, 255), [x, y], R)
    bat_end1 = BAT_LEN * cos(φ), BAT_LEN * sin(φ)
    bat_end2 = [-x for x in bat_end1]
    pg.draw.line(display, (255, 255, 0), bat_end1, bat_end2)
    pg.display.update()

def f_point(t, x0, y0, vx, vy, φ0, ω):
    return distance(x0 + vx * t, y0 + vy * t, φ0 + ω * t)

def df_point(t, x0, y0, vx, vy, φ0, ω):
    x = x0 + vx * t
    y = y0 + vy * t
    φ = φ0 + ω * t
    s, c = sin(φ), cos(φ)
    return vx * s + x * ω * c - vy * c + y * ω * s

def f_circle(t, x0, y0, vx, vy, φ0, ω):
    d = distance(x0 + vx * t, y0 + vy * t, φ0 + ω * t)
    return abs(d) - R

def df_circle(t, x0, y0, vx, vy, φ0, ω):
    x = x0 + vx * t
    y = y0 + vy * t
    φ = φ0 + ω * t
    s, c = sin(φ), cos(φ)
    return (vx * s + x * ω * c - vy * c + y * ω * s) * sign(distance(x, y, φ))

x, y = 100, 50
vx, vy = 5, 10
ω = pi / 6  # radians per second
φ = 0  # radians

while True:
    if pg.QUIT in [e.type for e in pg.event.get()]: break
    dt = DT
    args = x, y, vx, vy, φ, ω
    if will_collide(*args, dt):
        t0 = dt / 2
        # t_intersect = newton_raphson(t0, f_point, df_point, args)
        t_intersect = newton_raphson(t0, f_circle, df_circle, args)
        print(t_intersect)
        x += vx * t_intersect
        y += vy * t_intersect
        φ += ω * t_intersect
        dt -= t_intersect
        vx *= -2
        vy *= 2
        ω *= -1.5
    x += vx * dt
    y += vy * dt
    φ += ω * dt
    display_all(x, y, φ)
    clock.tick(FPS)
