from random import randint
import pygame

dx = 3  # Speed in X direction
dy = 4  # Speed in Y direction
x = 100
y = 100
radius = 20

def sign(x):
    if x == 0: return 0
    return 1 if x > 0 else -1

def rand_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
color = (200, 200, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    clock.tick(30)  # Make sure 1/30 second has passed
    display.fill((100, 100, 100))  # Clear the screen
    x += dx
    y += dy
    pygame.draw.circle(display, color, (x, y), radius)  # Draw the ball
    if x < radius or x > 500 - radius:  # Outside of the screen in x?
        dx = -dx  # Change the motion direction in x
        dx += sign(dx)
        dy += sign(dy)
        color = rand_color()
    if y < radius or y > 300 - radius:  # Outside of the screen in y?
        dy = -dy  # Change the motion direction in y
        dx += sign(dx)
        dy += sign(dy)
        color = rand_color()
    pygame.display.update()  # Update the screen
