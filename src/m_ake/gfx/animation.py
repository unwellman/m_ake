import pygame as pg
import m_ake as mk

import yaml
import os.path
from enum import Enum
from collections import deque
import logging
logger = logging.getLogger("m_ake")
logger.setLevel("DEBUG")

class Animation_parameters (object):
    """
    Object for standardizing parameters that determine animation states

    Attributes:
        vel: pg.Vector2 velocity
        acc: pg.Vector2 acceleration of the sprite's proper frame of reference
            (i.e. zero in free-fall, upward when on the ground)
        omega: float angular velocity
        norm: float normal angle of surface sprite is locked to (should be
            relative to the sprite---not in absolute world coordinates)
        coll: bool True if the sprite is actually in contact with such a surface
        face: bool if the sprite is reflected
        override: {str, str} dict of control/logical animation overrides
    """
    defaults = {
        "vel": pg.Vector2(),
        "acc": pg.Vector2(),
        "omega": 0.0,
        "norm": 0.0,
        "coll": True,
        "face": False,
        "animation": None,
        "frame": 0,
        "counter": 1,
        "override": None,
    }
    types = Enum("types", [
        ("bool", 0),
        ("int", 1),
        ("value", 2),
        ("key", 3),
    ])
    type_map = {
        "vel_x": types.value,
        "vel_y": types.value,
        "acc_x": types.value,
        "acc_y": types.value,
        "omega": types.value,
        "norm": types.value,
        "coll": types.bool,
        "face": types.bool,
        "animation": types.key,
        "frame": types.int,
        "counter": types.int,
        "override": types.key,
    }

    def __init__ (self, **kwargs):
        self.__dict__.update(Animation_parameters.defaults)
        keys = Animation_parameters.defaults.keys()
        for key, val in kwargs.items():
            if key in keys:
                self.__dict__[key] = val

    def update (self, **params):
        """
        This method currently has no checking in place, so just be careful
        """
        for key, val in params.items():
            self.__dict__[key] = val

    def check (self, key, cond):
        if self.type_map[key] == self.types.value:
            return cond[0] <= self[key] <= cond[1]
        if self.type_map[key] == self.types.int:
            if isinstance(cond, int):
                return self[key] == cond
            else:
                return self[key] in cond
        else:
            return self[key] == cond

    def __getitem__ (self, item):
        if item == "vel_x":
            return self.__dict__["vel"].x
        return self.__dict__[item]

    def __setitem__ (self, key, val):
        self.__dict__[key] = val

class Decision_tree (object):
    """
    Not actually a tree, but (hopefully?) acyclic
    """
    def __init__ (self, stream, *, frame_times):
        """
        Parameters:
            stream: parsed yaml object taken from config.parameters
            frame_times: dict of {animation: [list of frame times]}
        """
        self.nodes = {}
        for dct in stream:
            node = Decision_node(dct)
            self.nodes[node.name] = node

        self.frame_times = frame_times

        self.__verify_tree()

    def __call__ (self, params):
        """
        """
        key = "root"
        cont = True
        while cont:
            cont, key = self.nodes[key](params)
        # Now key is the animation key
        if params["animation"] == key:
            if params["counter"] >= self.frame_times[key][params["frame"]]:
                frame = (params["frame"] + 1) % len(self.frame_times[key])
            else:
                frame = params["frame"]
        else:
            frame = 0
        return key, frame, params["face"]

    def __verify_tree (self):
        """
        Check the tree for structural validity
        i.e.
            - Has a root
            - All nodes connected to root
            - No cycles
        """
        pass

class Decision_node (object):
    """"""
    kinds = Enum("kinds", [
        ("switch", 0),
        ("animation", 1),
    ])
    def __init__ (self, dct):
        """"""
        self.name = dct["id"]

        keys = dct.keys()
        self.kind = None
        if "switch" in keys:
            self.kind = Decision_node.kinds.switch
            self.switch = dct["switch"]
            self.children = dct["children"]
        elif "animation" in keys:
            self.kind = Decision_node.kinds.animation
            self.animation = dct["animation"]
        else:
            raise ValueError("Parameter node must specify a switch or animation")

    def __call__ (self, params):
        if self.kind == Decision_node.kinds.switch:
            for key, cond in self.children.items():
                if params.check(self.switch, cond):
                    return True, key
            options = list(self.children.keys())
            return True, options[len(options) - 1] # Questionable default
        elif self.kind == Decision_node.kinds.animation:
            return False, self.animation

    def __repr__ (self):
        return self.name

from m_ake.gfx.sprite import Sprite
class Animated (Sprite):
    """
    [DEVELOPER] Consider splitting Sprite into a few subclasses including
    Animated_sprite or even Character_sprite

    Class for encapsulating 2-D sprites and their animations

    Attributes:
        frames: dict of {str: list of pygame.Surface}
        key: str to access frames
        frame: int to access animation frame
        pos: pygame.Vector2: world coordinates
    """
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        self.frames = {}
        self.frame_times = {}
        self.next = None
        self.tree = None
        self.counter = 0.0
        self.params = Animation_parameters()
        self.frame_time = 46.269269269

    def update (self, dt, **kwargs):
        """
        Pass physics and input data to the sprite and prompt it to select
        the next animation
        """
        self.counter += 1000*dt
        self.pos = kwargs.pop("pos")
        self.theta = kwargs.pop("theta")
        if self.counter >= self.frame_time:
            while self.counter >= self.frame_time:
                self.counter -= self.frame_time
            self.resolve_tree(**kwargs)

    def resolve_tree (self, **kwargs):
        self.params.update(**kwargs)
        key, frm, face = self.tree(self.params)
        if self.params["animation"] == key and \
                self.params["frame"] == frm:
            self.params["counter"] += 1
        else:
            self.params.update(**{
                "animation": key,
                "frame": frm,
                "counter": 1,
            })
        surf = self.frames[key][frm]
        if face:
            surf = pg.transform.flip(surf, True, False)
        self.next = surf

    def get_blit_args (self, camera_theta=0.0):
        """
        Return args for a surface to call blit()

        Parameters:
            camera_theta: angle of view
        """
        surf = pg.transform.rotate(self.next, camera_theta - self.theta)
        return surf, self.pos

    def load_config (self, fp):
        """
        Load a sprite sheet using a YAML config (spec elsewhere)

        Parameters:
            fp: path-like for the YAML config file
        """
        with open(fp) as cfg:
            config = yaml.load(cfg, Loader=yaml.Loader)
        basename = config["metadata"]["fp"]
        dirname = os.path.split(fp)[0]
        img_fp = mk.get_path(os.path.join(dirname, basename))
        surf = pg.image.load(img_fp)
        w_h = (int(config["metadata"]["width"]), \
               int(config["metadata"]["height"]))
        name = config["metadata"]["name"]
        for anim in config["animations"]:
            self.__load_animation(name, anim, surf, w_h)

        self.tree = Decision_tree(config["parameters"],
            frame_times=self.frame_times)

        try:
            self.next = self.frames["idle"][0]
        except KeyError:
            pass

    def __load_animation (self, name, anim, surf, w_h):
        anim_id = anim["id"]
        frames = []
        for i in range(anim["frames"]):
            x = int(anim["x_offsets"][i])
            y = int(anim["y_offsets"][i])
            t = int(anim["f_times"][i])
            subsurf = surf.subsurface((x, y), w_h)
            subsurf = pg.transform.flip(subsurf, False, True)
            frames.append(subsurf)
        self.frames[anim_id] = frames
        self.frame_times[anim_id] = anim["f_times"]

    def __default_config_path (self, fp_img):
        fp, _ = os.path.splitext(fp_img)
        return fp + ".yml"

