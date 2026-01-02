import pygame as pg
import numpy as np
import yaml
import os

import m_ake as mk
import logging
logger = logging.getLogger("m_ake")

def cumulative_simpson (y, x):
    """
    Numpy-only implementation. y and x must be 1-dimensional and have the
    same dimensions. x must have evenly spaced samples for correct results.

    Note that the return shape has half the entries of y.
    """
    n, = y.shape
    res = np.zeros((n//2))
    dx = x[1] - x[0] # Pinky promise?
    res[0] = 0.0
    res[1] = 1/3 * dx * (y[0] + y[1])
    for i in np.arange(2, n//2):
        res[i] = 1/3 * dx * (y[0] + y[i]
            + 4*np.sum(y[1:i-1:2]) + 2*np.sum(y[2:i-2:2]))
    return res

class Material (object):
    """
    The visible part of world materials
    """
    def __init__ (self, data, texture, rotations=72):
        """
        Parameters:
            data (dict): dictionary loaded from a YAML specification
            texture: a pg.Surface to take textures from
        """
        self.name = data["id"] # Note that this should be unique!
        self.scale = data["scale"]
        rect = pg.Rect(data["offset"], data["size"])
        self.original = texture.subsurface(rect)
        self.load_rotations(self.original, rotations)
        self.round = rotations / 360
        self.rotations = rotations

    def load_rotations (self, surf, rotations):
        self.positions = []
        angles = np.linspace(0, 360, num=rotations, endpoint=False)
        for theta in angles:
            rot = pg.transform.rotate(surf, theta)
            self.positions.append(rot)

    def __call__ (self, theta):
        """
        Return a surface representing the material at the given rotation
        """
        idx = int(np.rint(-theta*self.round)) % self.rotations
        return self.positions[idx]

class World_importer (object):
    """
    Many functions used for world geometry and file storage
    """
    def __init__ (self, world_fp):
        """
        Parameters:
            world_fp: location of YAML world description, returned from
                mk.get_path
        """
        self.fp = world_fp
        with open(self.fp) as stream:
            world = yaml.load(stream, Loader=yaml.Loader)

        basename = world["metadata"]["material_fp"]
        surf = pg.image.load(self.get_relative_path(basename))
        self.init_materials(world["materials"], surf)
        self.init_geometry(world["geometry"])
        self.init_player(world["player"])

    def get_relative_path (self, basename):
        dirname = os.path.split(self.fp)[0]
        return mk.get_path(os.path.join(dirname, basename))

    def init_player (self, data):
        self.player = mk.gfx.Animated()
        config = self.get_relative_path(data["fp"])
        self.player.load_config(config)

        code = f"{data['controller']}"
        actor_cls = eval(code)
        assert issubclass(actor_cls, mk.physics.Actor)
        self.controller = actor_cls(**data)
        self.controller.register(self.player)

    def init_materials (self, data, surf):
        """
        Load and store materials
        """
        self.materials = {}
        for material in data:
            mat = Material(material, surf)
            self.materials[material["id"]] = mat

    def init_geometry (self, data):
        """
        Computation for splines, generating colliders, etc.
        """
        initializers = {
            "parametric": self.init_parametric,
        }
        self.geometry = {}
        for dct in data:
            actor, sprite = initializers[dct["shape"]](dct)
            actor.register(sprite)
            self.geometry[dct["id"]] = (actor, sprite)

    def init_parametric (self, dct):
        data = dct["data"]
        code_x = data.pop("x")
        code_y = data.pop("y")
        x = lambda t: eval(code_x)
        y = lambda t: eval(code_y)
        points = self.sample_arc_points(x, y, **data)
        loop = dct["data"]["cycle"]
        params = {
            "pos": pg.Vector2(dct["origin"]),
            "loop": loop,
        }
        try:
            if dct["walkable"]:
                actor = mk.physics.shapes.Parametric_path(points, **params)
            else:
                actor = mk.physics.shapes.Parametric(points, **params)
        except KeyError:
            actor = mk.physics.shapes.Parametric(points, **params)
        material = self.materials[dct["material"]]
        from m_ake.gfx.world_sprites import Parametric
        sprite = Parametric(material, points)
        return actor, sprite
    
    @classmethod
    def sample_arc_points (cls, x, y, *, parameter=[0, 1], scale=16,
                           arc_sample=1000, cycle=False, **kwargs):
        """
        Take a dictionary of parameters for a parametric curve, then return
        a np.array of equal-arc length samples

        Parameters:
            x: callable returning x value given a parameter t
            y: callable returning y value given a parameter t
            parameter: start and end values of the parameter
            scale: target size of samples
            arc_sample: Initial number of arc length samples per line segment.
        """
        n = 2*arc_sample # double samples for Simpson's rule
        mi, ma = min(parameter), max(parameter)
        if cycle:
            t = np.linspace(mi, ma, num=n, endpoint=False)
            t = np.append(t, mi)
        else:
            t = np.linspace(mi, ma, num=n+1, endpoint=True)
        x = x(t)
        y = y(t)
        x_t = np.gradient(x, t)
        y_t = np.gradient(y, t)

        s_t = np.sqrt(x_t**2 + y_t**2)
        s = cumulative_simpson(s_t, t)
        sample_length = s[-1] / np.round(s[-1] / scale)/2

        idx = [0]
        over = False
        i = 1
        while s[idx[-1]] + sample_length < s[-1]:
            # Condition ensures stop roughly 1 sample length before the end
            j = idx[-1]
            while s[j] < i*sample_length:
                j += 1
            if over:
                j -= 1
                assert j > idx[-1]
            over = not over
            idx.append(j)
            i += 1
        ret = [[], []]
        for i in idx:
            # Multiply indices by 2 because the integrator returns 1/2 size
            ret[0].append(x[2*i])
            ret[1].append(y[2*i])

        # Remove the penultimate point if it is too close to the end
        if (ret[0][-1]-x[-1])**2 + (ret[1][-1]-y[-1])**2 <= sample_length/2:
            ret[0].pop(-1)
            ret[1].pop(-1)

        # Ensure that the end or cycle point is included
        ret[0].append(x[-1])
        ret[1].append(y[-1])

        return np.asarray(ret)
