import random
import pygame as pg
pg.init()

clock = pg.time.Clock()
road = pg.image.load('four-lane-road.jpg')
road_size = road.get_size()
step = [wh / 4 for wh in road_size]

places = [(i % 4 + random.random()*0.4 - 0.2, i // 4) for i in range(16)]
random.shuffle(places)
places = places[:7]

vehicles = [f'vehicle/{i}.png' for i in range(14)]
random.shuffle(vehicles)
vehicles = [pg.image.load(v) for v in vehicles[:7]]

for i, place in enumerate(places):
    angle = 90 if place[1] in (0, 1) else -90
    angle += random.random() * 2 - 1
    vehicles[i] = pg.transform.rotate(vehicles[i], angle)
    vehicles[i].set_colorkey((0, 255, 255))

display = pg.display.set_mode(road_size)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    display.blit(road, (0, 0))
    for place, vehicle in zip(places, vehicles):
        size = vehicle.get_size()
        place = [(place[i] + 0.5)*step[i] - size[i] / 2 for i in (0, 1)]
        display.blit(vehicle, place)
    pg.display.update()
    clock.tick(30)
