import pytest
from m_ake import __main__
import m_ake as mk
import pygame as pg

fp_b = "res/programmer_assets/blue_border.png"
fp_w = "res/programmer_assets/white_border.png"
lucy_fp = "res/programmer_assets/lucy.png"

def test_integration_animation ():
    scn = mk.gfx.Screen((320, 180))
    disp = pg.display.set_mode((1280, 720))
    bkgnd = mk.gfx.Sprite()
    avatar = mk.gfx.Sprite()
    bkgnd.load_image(fp_b, "blue", set_frame=True)
    avatar.load_sheet(lucy_fp)
    avatar.set_frame("idle")
    avatar.queue_animation("idle", loop=True)
    scn.register(bkgnd, end=False)
    scn.register(avatar)
    scn.clear_color = pg.Color(48, 48, 48)
    x = 28
    y = 74
    dt = 0
    frame = 0
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pressed = pg.key.get_just_pressed()
        if pressed[pg.K_e]:
            avatar.clear_animation()
            avatar.queue_animation("hair")
            avatar.queue_animation("idle", loop=True)
        elif pressed[pg.K_d]:
            avatar.clear_animation()
            avatar.queue_animation("run", loop=True)
        elif pressed[pg.K_a]:
            avatar.clear_animation()
            avatar.queue_animation("run_left", loop=True)

        held = pg.key.get_pressed()
        if held[pg.K_d]:
            x += 3
        if held[pg.K_a]:
            x -= 3
        avatar.pos = (x, y)

        released = pg.key.get_just_released()
        if released[pg.K_d]:
            avatar.clear_animation()
            avatar.queue_animation("idle", loop=True)
        if released[pg.K_a]:
            avatar.clear_animation()
            avatar.queue_animation("idle_left", loop=True)

        scn.draw()
        scn.upscale(disp)
        pg.display.flip()

        dt = clock.tick(24)
        frame += 1

    pg.quit()

    pass

def test_main ():
    __main__.main()

