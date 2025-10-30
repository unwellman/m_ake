import m_ake as mk
import pygame as pg

fp_w = "res/programmer_assets/white_border.png"
fp_b = "res/programmer_assets/blue_border.png"

def test_screen_init ():
    scn = mk.gfx.Screen((320, 180))

def test_screen_clear ():
    scn = mk.gfx.Screen((320, 180))
    scn.clear_color = pg.Color(48, 96, 130)
    scn.draw()
    assert scn.get_at((0, 0)) == pg.Color(48, 96, 130)

def test_screen_register ():
    scn = mk.gfx.Screen((320, 180))
    spt_1 = mk.gfx.Sprite()
    scn.register(spt_1)

def test_screen_draw ():
    scn = mk.gfx.Screen((320, 180))
    spt_1 = mk.gfx.Sprite()
    spt_1.load_image(fp_w, "white", set_frame=True)
    scn.register(spt_1)
    scn.draw()

def test_screen_upscale ():
    pg.init()
    disp = pg.Surface((1280, 720))
    scn = mk.gfx.Screen((320, 180))
    scn.draw()
    scn.upscale(disp)

