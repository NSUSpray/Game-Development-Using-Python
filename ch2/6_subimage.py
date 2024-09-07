import pygame as pg

pg.init()

def is_quit(event):
    return (event.type == pg.QUIT
        or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)

def get_rect(pos1, pos2):
    pos = min(pos1[0], pos2[0]), min(pos1[1], pos2[1])
    size = [max(p1, p2) - p for p1, p2, p in zip(pos1, pos2, pos)]
    return pos, size

def get_orig_rect(rect, pos, factor):
    pos = [(xy - p) / f for xy, p, f in zip(rect[0], pos, factor)]
    size = [wh / f for wh, f in zip(rect[1], factor)]
    return pos, size

orig = pg.image.load('nonformal_piter.jpg')
orig_size = orig.get_size()
factor = 1/5, 1/5
win_size = surf_size = [wh * f for wh, f in zip(orig_size, factor)]
surf = pg.transform.smoothscale(orig, surf_size)
display = pg.display.set_mode(win_size)
surf_pos = 0, 0
display.blit(surf, surf_pos)
pg.display.flip()

running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if is_quit(event):
            running = False
            break
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            mouse_rect = get_rect(mouse_pos, event.pos)
            factor = [wh / owh for wh, owh in zip(surf_size, orig_size)]
            pos, size = get_orig_rect(mouse_rect, surf_pos, factor)
            factor = [wh / owh for wh, owh in zip(size, win_size)]
            surf_pos = [-xy / f for xy, f in zip(pos, factor)]
            surf_size = [os * ws / s for os, ws, s in zip(orig_size, win_size, size)]
            surf = pg.transform.smoothscale(orig, surf_size)
            display.blit(surf, surf_pos)
            pg.display.flip()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            pg.image.save(display, 'output.jpg')
    clock.tick(60)

pg.quit()
