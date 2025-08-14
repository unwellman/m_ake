import pygame as pg
import os.path
import yaml
from collections import deque

class Sprite (object):
    """
    Class for encapsulating 2-D sprites and their animations

    Attributes:
        frames: dict of {str: list of pygame.Surface}
        key: str to access frames
        frame: int to access animation frame
        pos: pygame.Vector2: screen-space coordinates
    """
    def __init__ (self):
        self.frames = {}
        self.queue = deque()
        self.loop = None
        self.default = (None, 0)
        self.pos = pg.Vector2(0, 0)

    def load_image (self, fp, kw=None, set_frame=False):
        """
        Load an image and map it to a keyword (default is same as fp)

        Parameters:
            fp: file-like object for pygame.image
            kw: hashable key for the image data
        """
        if kw is None:
            kw = fp
        self.frames[kw] = [pg.image.load(fp)]
        if set_frame:
            self.set_frame(kw)

    def load_sheet (self, fp_img, fp_cfg=None):
        """
        Load a sprite sheet using a metadata file to generate animations

        Parameters:
            fp_img: file-like object for the sprite sheet
            fp_cfg: file-like for YAML config---spec WIP. Defaults to 
                same filename as fp_img with extension changed to .yml.
        """
        if fp_cfg is None:
            fp_cfg = self.__default_config_path (fp_img)

        with open(fp_cfg) as cfg:
            config = yaml.load(cfg, Loader=yaml.Loader)
        surf = pg.image.load(fp_img)
        w_h = (int(config["metadata"]["width"]), \
               int(config["metadata"]["height"]))
        name = config["metadata"]["name"]
        for anim in config["animations"]:
            self.__load_animation(name, anim, surf, w_h)

    def __load_animation (self, name, anim, surf, w_h):
        anim_id = anim["id"]
        frames = []
        for i in range(anim["frames"]):
            x = int(anim["x_offsets"][i])
            y = int(anim["y_offsets"][i])
            t = int(anim["f_times"][i])
            subsurf = surf.subsurface((x, y), w_h)
            for j in range(t):
                # Enables animating on ones, twos, etc.
                frames.append(subsurf)
        self.frames[anim_id] = frames

    def __default_config_path (self, fp_img):
        fp, _ = os.path.splitext(fp_img)
        return fp + ".yml"

    def set_frame (self, kw, frame=0):
        """
        Set the default frame to be returned when .get_blit_args() is called

        Parameters:
            kw: hashable key previously assigned with .load_image()
            frame: index for the frame within the key, default 0
        """
        assert kw in self.frames.keys()
        assert frame < len(self.frames[kw])
        self.default = (kw, frame)

    def queue_animation (self, kw, loop=False):
        """
        Queue a sequence of frames to be returned by succeeding calls to
        get_blit_args()
        """
        self.queue.extend(self.frames[kw])
        if loop:
            self.loop = kw
        else:
            self.loop = None

    def clear_animation (self):
        """
        Clear all animation frames
        """
        self.queue.clear()
        self.loop = None

    def get_blit_args (self, camera_pos=pg.Vector2(0, 0)):
        """
        Return args for a surface to call blit()
        """
        if self.queue:
            return self.queue.popleft(), (self.pos - camera_pos)
        elif self.loop:
            self.queue_animation(self.loop, loop=True)
            return self.queue.popleft(), (self.pos - camera_pos)

        kw, frame = self.default
        return self.frames[kw][frame], self.pos



