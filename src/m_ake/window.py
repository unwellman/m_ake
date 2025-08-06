import pygame as pg
import m_ake as mk

class Window:
    def __init__ (self, *args, **kwargs):
        params = {
            'size': (mk.config.width, mk.config.height),
        }
        self.surface = pg.display.set_mode(**params)

