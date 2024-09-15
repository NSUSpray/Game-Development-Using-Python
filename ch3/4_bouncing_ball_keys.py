import pygame
dx = 3  # Speed in X direction
dy = 4  # Speed in Y direction
x = 100
y = 100
radius = 20
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((500, 300), pygame.SRCALPHA, 32)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    dx += 1 if dx > 0 else -1
                    dy += 1 if dy > 0 else -1
                case pygame.K_s:
                    dx -= 1 if dx > 0 else -1
                    dy -= 1 if dy > 0 else -1
    clock.tick(30)  # Make sure 1/30 second has passed
    display.fill((100, 100, 100))  # Clear the screen
    x += dx
    y += dy
    pygame.draw.circle(display, (200, 200, 200), (x, y), radius)  # Draw the ball
    if x < radius or x > 500 - radius:  # Outside of the screen in x?
        dx = -dx  # Change the motion direction in x
    if y < radius or y > 300 - radius:  # Outside of the screen in y?
        dy = -dy  # Change the motion direction in y
    pygame.display.update()  # Update the screen
