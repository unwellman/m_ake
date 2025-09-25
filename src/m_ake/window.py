import pygame as pg
import m_ake as mk

class Window:
    def __init__ (self, *args, **kwargs):
        f = mk.config.pixel_factor
        self.params = {
            "size": (f*mk.config.width, f*mk.config.height),
            "flags": pg.FULLSCREEN,
        }
        self.surface = pg.display.set_mode(**self.params)
        self.screen = None

    def bind_screen (self, screen):
        self.screen = screen

    def __call__ (self):
        self.surface.fill("black")
        self.screen.upscale(self.surface)
        pg.display.flip()

