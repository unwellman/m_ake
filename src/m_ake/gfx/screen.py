import pygame as pg
import m_ake as mk
from collections import deque
import logging
logger = logging.getLogger("m_ake")

class Camera (object):
    def __init__ (self, radius, pos=pg.Vector2(0, 0), theta=0.0):
        self.radius = radius
        self.pos = pos
        self.theta = theta

class Screen (pg.Surface):
    """
    Object for preparing data for rendering to the screen
    """
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = pg.Vector2(self.get_size())/2
        self.camera = Camera(self.offset.magnitude())
        self.factor = mk.config.pixel_factor
        self.__col = pg.Color(0, 0, 0, 255)
        self.sprites = deque()
    
    @property
    def clear_color (self):
        return self.__col

    @clear_color.setter
    def clear_color (self, col):
        self.__col = pg.Color(col)

    def reposition (self, pos, theta=0.0):
        """
        Discontinuously reposition the camera. Intended for use by a 
        physics module with better control (for now).
        """
        self.camera.pos = pg.Vector2(pos)
        self.camera.theta = theta

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
        blits = []
        for spt in self.sprites:
            surf, pos = spt.get_blit_args(self.camera)
            surf = pg.transform.flip(surf, False, True)
            pos = pos - self.camera.pos
            pos = pos.rotate(-self.camera.theta)
            pos.y = -pos.y
            pos = pos - 1/2 * pg.Vector2(surf.size) + self.offset
            blits.append((surf, pos))
        self.blits(blits, doreturn=0)

    def upscale (self, surf):
        """
        Upscale the screen and blit it onto a surface
        """
        surf.blit(pg.transform.scale_by(self, self.factor))

