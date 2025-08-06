import pygame as pg
import m_ake as mk


class Screen (pg.Surface):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factor = mk.config.pixel_factor

    def upscale (self, surf):
        """
        Upscale the screen and draw it to surf
        """
        pg.transform.scale_by(self, self.factor, dest_surface=surf)

