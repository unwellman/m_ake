import pygame as pg

class Sprite (object):
    def __init__ (self):
        self.frames = {}
        self.key = None

    def load_image (self, fp, kw=None):
        """
        Load an image and map it to a keyword (default is same as fp)

        Parameters:
            fp: file-like object for pygame.image
            kw: hashable key for the image data
        """
        if kw is None:
            kw = fp
        self.frames[kw] = pg.image.load(fp)

    def set_frame (self, kw):
        """
        Set the frame to be returned when .get_surf() is called

        Parameters:
            kw: hashable key previously assigned with .load_image()
        """
        assert kw in self.frames.keys()
        self.key = kw

    def get_surf (self):
        """
        Return the sprite's surface object to be drawn
        """
        return self.frames[self.key]


