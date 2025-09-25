import pygame as pg
import os.path
import yaml
from collections import deque

class Animation_parameters (object):
    """
    Object for holding parameters that determine animation states

    Attributes:
        vel: pg.Vector2 velocity
        acc: pg.Vector2 acceleration (does not need to be the physics engine
            acceleration---for example, freefall can be an inertial frame)
        omega: float angular velocity
        norm: float normal of surface sprite is locked to (should be relative
            to the sprite---not in absolute world coordinates)
        coll: bool True if the sprite is actually in contact with such a surface
        face: bool if the sprite is reflected
        override: {str, str} dict of control/logical animation overrides
    """

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
        self.theta = 0.0

    def update (self, dt, **kwargs):
        """
        Pass physics and input data to the sprite and prompt it to select
        the next animation
        """
        self.pos = kwargs["pos"]
        self.theta = kwargs["theta"]

        if self.queue:
            self.queue.popleft()
        if not self.queue:
            if self.loop:
                self.queue_animation(self.loop, loop=True)
            else:
                kw, frame = self.default
                self.queue.append(self.frames[kw][frame])

    def get_blit_args (self, advance=True):
        """
        Return args for a surface to call blit()

        Parameters:
            camera_pos: offset for blit args (Should this even be passed here?)
            advance: pops frame if True, does not interfere otherwise
        """
        surf = pg.transform.rotate(self.queue[0], self.theta)
        offset = 1/2 * pg.Vector2(surf.get_width(), surf.get_height())
        pos = self.pos - offset
        return surf, pos

    def get_hitbox (self):
        """
        Get the current collision state for this sprite as defined in the
        """
        if self.queue:
            return self.queue[0], self.pos
        kw, frame = self.default
        return self.frames[kw][frame], self.pos

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
        DEPRECATED
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

    def load_config (self, fp):
        """
        Load a sprite sheet using a YAML config (spec elsewhere)

        Parameters:
            fp: path-like for the YAML config file
        """

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


