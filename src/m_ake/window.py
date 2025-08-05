import pygame as pg
from m_ake import config


class Window:
    def __init__ (self, *args, **kwargs):
        params = {
            'size': (config.width, config.height),
        }
        self.screen = pg.display.set_mode(**params)

