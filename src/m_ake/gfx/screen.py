import pygame as pg
import m_ake as mk
from collections import deque

class Screen (pg.Surface):
    """
    Object for preparing data for rendering to the screen
    """
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factor = mk.config.pixel_factor
        self.__col = pg.Color(0, 0, 0, 255)
        self.sprites = deque()
    
    @property
    def clear_color (self):
        return self.__col

    @clear_color.setter
    def clear_color (self, col):
        self.__col = pg.Color(col)

    def register (self, spt, end=True):
        """
        Register a sprite to be drawn succeeding draw() calls

        Parameters:
            spt: a gfx.Sprite object
            end: determines which end of the queue to append to, default last
        """
        if end:
            self.sprites.append(spt)
        else:
            self.sprites.appendleft(spt)

    def clear (self):
        """
        Clear all registered sprites
        """
        self.sprites.clear()

    def draw (self):
        """
        Draw registered sprites in their order in the deque
        """
        self.fill(self.__col)
        for spt in self.sprites:
            args = spt.get_blit_args()
            self.blit(*args)

    def upscale (self, surf):
        """
        Upscale the screen and blit it onto a surface
        """
        surf.blit(pg.transform.scale_by(self, self.factor))

