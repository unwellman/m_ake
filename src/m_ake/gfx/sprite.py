import pygame as pg

class Sprite (object):
    def __init__ (self):
        self.frames = {}
        self.key = None
        self.pos = (0, 0)

    def load_image (self, fp, kw=None, set_frame=False):
        """
        Load an image and map it to a keyword (default is same as fp)

        Parameters:
            fp: file-like object for pygame.image
            kw: hashable key for the image data
        """
        if kw is None:
            kw = fp
        self.frames[kw] = pg.image.load(fp)
        if set_frame:
            self.set_frame(kw)

    def set_frame (self, kw):
        """
        Set the frame to be returned when .get_blit_args() is called

        Parameters:
            kw: hashable key previously assigned with .load_image()
        """
        assert kw in self.frames.keys()
        self.key = kw

    def get_blit_args (self):
        """
        Return args for a surface to call blit()
        """
        return self.frames[self.key], self.pos


