import m_ake as mk
import pygame as pg

def test_sprite_init ():
    spt = mk.gfx.Sprite()

def test_sprite_load ():
    border_fp = "res/programmer_assets/white_border.png"
    spt = mk.gfx.Sprite()
    spt.load_image(border_fp)

def test_sprite_set ():
    fp_w = "res/programmer_assets/white_border.png"
    spt = mk.gfx.Sprite()
    spt.load_image(fp_w, "white")
    spt.set_frame("white")

def test_sprite_get ():
    fp_w = "res/programmer_assets/white_border.png"
    fp_b = "res/programmer_assets/blue_border.png"
    spt = mk.gfx.Sprite()
    spt.load_image(fp_w, "white")
    spt.load_image(fp_b, "blue")
    spt.set_frame("blue")
    col = spt.get_surf().get_at((0, 0))
    assert col == pg.Color(48, 96, 130)
    spt.set_frame("white")
    col = spt.get_surf().get_at((0, 0))
    assert col == pg.Color(255, 255, 255)


def test_screen_init ():
    pass

def test_screen_register ():
    pass

def test_screen_upscale ():
    pass

