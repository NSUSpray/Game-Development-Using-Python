from dataclasses import dataclass
from math import sin, cos, sqrt, pi, atan, atan2
from random import random
from typing import Self

import pygame as pg


W, H = 800, 600
ROAD_WIDTH = 100
ELLIPSE_A = W/2 - ROAD_WIDTH/2
ELLIPSE_B = H/2 - ROAD_WIDTH/2
NUM_OF_WAYPOINTS = 8
FPS = 60.0 
DT = 1 / FPS

pg.init()
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()


'''def radius_of_curvature(sin: float, cos: float) -> float:
    s, c, a, b = sin, cos, ELLIPSE_A, ELLIPSE_B
    return (b*b*c*c + a*a*s*s)**1.5 / (a * b)'''


def plus_minus_pi(angle):
    if angle > 180:
        angle -= 360
    elif angle <= -180:
        angle += 360
    return angle


@dataclass
class Point:
    x: float
    y: float
    def distance(self, A: 'Point') -> float:
        return sqrt((self.x - A.x)**2 + (self.y - A.y)**2)
    def angle(self, A: 'Point') -> float:
        return atan2(A.y - self.y, A.x - self.x)


@dataclass
class Waypoint(Point):
    desired_v: float
    prev_: Self|None = None
    next_: Self|None = None
    def draw(self) -> pg.Rect:
        return pg.draw.circle(display, (63, 63, 95), (self.x, self.y), self.desired_v / 30)


class Vehicle(Point):

    image = pg.image.load('police.png')
    cruise_v = 300.0
    a_min = -100.0
    a_max = 100.0
    a_k = 10.0
    # dist_threshold = ROAD_WIDTH / 2
    dist_factor = 0.03
    omega = 250.0

    def __init__(self, x: float, y: float, phi: float) -> None:
        self.x = x
        self.y = y
        self.phi = phi
        self.v = 0.0
        self.o = 0.0  # angle speed
        self.a = 0.0
        self.image.set_colorkey((0, 255, 255))

    def line_distance(self, A: Waypoint, B: Waypoint) -> float:
        S = (B.y - A.y) * self.x - (B.x - A.x) * self.y + B.x*A.y - B.y*A.x
        D = A.distance(B)
        return S / D

    def draw(self) -> pg.Rect:
        rotated = pg.transform.rotate(self.image, -(self.phi + 90))
        w, h = rotated.get_size()
        return display.blit(rotated, (self.x - w/2, self.y - h/2))

    def move(self, desired_v: float, A: Waypoint, B: Waypoint) -> Self:
        if self.v < desired_v:
            self.a = min(self.a_max, self.a_k * (desired_v - self.v))
        elif self.v > desired_v:
            self.a = max(self.a_min, self.a_k * (desired_v - self.v))
        self.v += self.a * DT

        dist = self.line_distance(A, B)
        '''if dist < -self.dist_threshold:
            self.phi -= self.omega
        elif dist > self.dist_threshold:
            self.phi += self.omega'''
        to_road = atan(dist * self.dist_factor) * 180/pi
        AB = A.angle(B) * 180/pi
        desired_phi = to_road + AB
        self.o = self.omega * plus_minus_pi(desired_phi - self.phi) / 180

        self.phi = plus_minus_pi(self.phi + self.o * DT)
        phi_rad = self.phi * pi/180
        self.x += self.v * cos(phi_rad) * DT
        self.y += self.v * sin(phi_rad) * DT

        return self


def ellipse_waypoints() -> list[Waypoint]:
    waypoints = []
    for i in range(NUM_OF_WAYPOINTS):
        phi = 2*pi / NUM_OF_WAYPOINTS * i
        s, c = sin(phi), cos(phi)
        x = ELLIPSE_A * c + W/2
        y = ELLIPSE_B * s + H/2
        '''R = radius_of_curvature(s, c)
        desired_v = Vehicle.cruise_v * (1 - exp(-R / 300))'''
        desired_v = Vehicle.cruise_v * (0.5 + random())
        w = Waypoint(x, y, desired_v)
        waypoints.append(w)
    for i in range(NUM_OF_WAYPOINTS):
        waypoints[i].prev_ = waypoints[i - 1]
        waypoints[i].next_ = waypoints[(i + 1) % NUM_OF_WAYPOINTS]
    return waypoints


character = Vehicle(random() * 800, random() * 600, random() * 360 - 180)
waypoints = ellipse_waypoints()
'''waypoints = [
    Waypoint(25, 375, 200),
    Waypoint(775, 25, 0),
]'''

wp_dists = list(map(character.distance, waypoints))
closest_index = wp_dists.index(min(wp_dists))
A = waypoints[closest_index]
B = A.next_

while True:
    if pg.QUIT in [e.type for e in pg.event.get()]: break
    if B:
        if character.distance(B) < character.distance(A):
            A = B
            B = A.next_
        if B:
            dA, dB = map(character.distance, [A, B])
            desired_v = (dA * B.desired_v + dB * A.desired_v) / (dA + dB)
            character.move(desired_v, A, B)
    display.fill((0, 127, 0))
    pg.draw.ellipse(display, [63]*3, (0, 0, W, H), ROAD_WIDTH)
    for w in waypoints: w.draw()
    character.draw()
    pg.display.update()
    clock.tick(FPS)
