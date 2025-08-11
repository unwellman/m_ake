import m_ake as mk
import pygame as pg

fp_w = "res/programmer_assets/white_border.png"
fp_b = "res/programmer_assets/blue_border.png"
char = "res/assets/you.png"
conf = "res/assets/you.yml"

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

def test_sprite_sheet ():
    spt = mk.gfx.Sprite()
    spt.load_sheet(char, conf)

def test_sprite_sheet_default_fp ():
    spt = mk.gfx.Sprite()
    spt.load_sheet(char)

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

def test_gfx_integration_1 ():
    scn = mk.gfx.Screen((320, 180))
    disp = pg.display.set_mode((1280, 720))
    bkgnd = mk.gfx.Sprite()
    avatar = mk.gfx.Sprite()
    bkgnd.load_image(fp_b, "blue", set_frame=True)
    avatar.load_sheet(char)
    avatar.set_frame('you_idle')
    scn.register(bkgnd, end=False)
    scn.register(avatar)
    scn.clear_color = pg.Color(127, 127, 127)
    x = 128
    y = 0
    dt = 0
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if pg.key.get_pressed()[pg.K_s]:
            y += 1
        if pg.key.get_just_pressed()[pg.K_s]:
            avatar.queue_animation('you_walk_S', loop=True)
        if pg.key.get_just_released()[pg.K_s]:
            avatar.clear_animation()
        avatar.pos = (x, y)

        scn.draw()
        scn.upscale(disp)
        pg.display.flip()

        dt = clock.tick(30)

    pg.quit()


