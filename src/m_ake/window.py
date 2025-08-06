import pygame as pg
import m_ake as mk

class Window:
    def __init__ (self, *args, **kwargs):
        params = {
            'size': (mk.config.width, mk.config.height),
        }
        self.surface = pg.display.set_mode(**params)
        self.screen = None

    def bind_screen (self, screen):
        self.screen = screen

    def __call__ (self):
        self.surface.fill("black")
        self.screen.upscale(self.surface)
        pg.display.flip()

