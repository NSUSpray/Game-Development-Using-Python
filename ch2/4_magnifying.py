import pygame as pg

FACTOR = 1/5
pg.init()

def is_quit(event):
    return (event.type == pg.QUIT
        or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE))

def get_surf_pos(pos, size):
    return [xy - wh//2 for xy, wh in zip(pos, size)]

orig = pg.image.load('nonformal_piter.jpg')
bg = pg.transform.smoothscale_by(orig, FACTOR)
bgsize = bg.get_size()
display = pg.display.set_mode(bgsize)

surf = pg.Surface([wh * 0.2 for wh in bgsize])
surf_size = surf.get_size()
running = True
pos = None
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if is_quit(event):
            running = False
            break
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = None if pos else event.pos
        elif event.type == pg.MOUSEMOTION:
            pos = pos and event.pos
    display.blit(bg, (0, 0))
    if pos:
        orig_pos = [-xy / FACTOR for xy in pos]
        surf.blit(orig, orig_pos)
        surf_pos = get_surf_pos(pos, surf_size)
        display.blit(surf, surf_pos)
    pg.display.flip()
    clock.tick(60)

pg.quit()
