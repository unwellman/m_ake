import m_ake as mk
import pygame as pg
from abc import ABC, abstractmethod

class Sprite (ABC):
    """
    Base class for things drawn to the screen

    Attributes:
        pos (pg.Vector2): position in world coordinates
        theta (float): Angular position relative to world x-axis
    """
    def __init__ (self, **kwargs):
        try:
            self.pos = kwargs["pos"]
        except KeyError:
            self.pos = pg.Vector2(0, 0)
        try:
            self.theta = kwargs["theta"]
        except KeyError:
            self.theta = 0.0

    @abstractmethod
    def get_blit_args (self, camera):
        """
        Return at least a surface and position to be passed to
        pg.Surface.blit()
        """

class Drawable (pg.Surface, Sprite):
    """
    A mk.Sprite that can be drawn on with pg.draw
    """
    def __init__ (self, size, **kwargs):
        pg.Surface.__init__(self, size, flags=pg.SRCALPHA)
        Sprite.__init__(self, **kwargs)

    def get_blit_args (self, camera):
        surf = pg.transform.rotate(self, camera.theta - self.theta)
        return surf, self.pos

class Static (Sprite):
    """
    Non-animated sprite
    """
    def load_image (self, fp, kw=None, set_frame=False):
        """
        Load an image and map a keyword to it

        Parameters:
            fp: file-like object for pygame.image
            kw: hashable key for the image data (defaults to filepath)
        """
        if kw is None:
            kw = fp
        self.frames[kw] = [pg.transform.flip(pg.image.load(fp), False, True)]
        if set_frame:
            self.set_frame(kw)

    def set_frame (self, kw, frame=0):
        """
        Set the default frame to be returned when .get_blit_args() is called

        Parameters:
            kw: hashable key previously assigned with .load_image()
            frame: index for the frame within the key, default 0
        """
        assert kw in self.frames.keys()
        assert frame < len(self.frames[kw])
        self.next = self.frames[kw][frame]


