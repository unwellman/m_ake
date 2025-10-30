import m_ake as mk
import pygame as pg

char = "res/assets/you.png"
fp_w = "res/programmer_assets/white_border.png"
fp_b = "res/programmer_assets/blue_border.png"
lucy_fp = "res/programmer_assets/lucy.png"
migu_fp = "res/programmer_assets/migu.yml"

def test_sprite_init ():
    spt = mk.gfx.Sprite()

def test_sprite_load ():
    spt = mk.gfx.Sprite()
    spt.load_image(fp_w)

def test_sprite_set ():
    spt = mk.gfx.Sprite()
    spt.load_image(fp_w, "white")
    spt.set_frame("white")

def test_sprite_get ():
    spt = mk.gfx.Sprite()
    spt.load_image(fp_w, "white")
    spt.load_image(fp_b, "blue")
    spt.set_frame("blue")
    surf, *_ = spt.get_blit_args()
    col = surf.get_at((0, 0))
    assert col == pg.Color(48, 96, 130)
    spt.set_frame("white")
    surf, *_ = spt.get_blit_args()
    col = surf.get_at((0, 0))
    assert col == pg.Color(255, 255, 255)


