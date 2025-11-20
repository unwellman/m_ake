import jax
import jax.numpy as jnp
from quadax import cumulative_simpson
import yaml

import m_ake as mk
import logging
logger = logging.getLogger("m_ake")

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
        with open(fp) as stream:
            world = yaml.load(stream, Loader=yaml.Loader)

        self.geometry = []

    def init_materials (self, world):
        """
        Load and store materials
        """

    def init_geometry (self, world):
        """
        Computation for splines, generating colliders, etc.
        """
        initializers = {
            "parametric": self.spline,
        }
        for dct in world["geometry"]:
            initializer = initializers[dct["shape"]]
            raise NotImplemented()
    
    @classmethod
    def spline (cls, dct):
        """
        Take a dictionary of parameters for a parametric curve, then return
        a jnp.array of equal-arc length samples

        Parameters:
            dct: Dict from world description file
            arc_sample: Number of arc length samples per line segment.
        """
        data = dct["data"]
        x = lambda t: eval(data["x"])
        y = lambda t: eval(data["y"])
        n = data["arc_sample"]
        rng = data["parameter"]
        mi, ma = min(rng), max(rng)
        if data["cycle"]:
            t = jnp.linspace(mi, ma, num=n, endpoint=False)
            t = jnp.append(t, mi)
        else:
            t = jnp.linspace(mi, ma, num=n+1, endpoint=True)
        x_t = jax.vmap(jax.grad(x))
        x_t = x_t(t)
        y_t = jax.vmap(jax.grad(y))
        y_t = y_t(t)

        s_t = jnp.sqrt(x_t**2 + y_t**2)
        s = cumulative_simpson(s_t, dx=(ma - mi)/n)
        sample_length = data["scale"]
        logger.debug(f"World spline {dct["id"]} sampling {sample_length}")

        idx = [0]
        over = False
        i = 1
        while s[idx[-1]] + sample_length < s[-1]:
            j = idx[-1]
            while s[j] < i*sample_length:
                j += 1
            if over:
                j -= 1
                assert j > idx[-1]
            over = not over
            idx.append(j)
            i += 1
        idx.append(len(s))
        ret = [[], []]
        for i in idx:
            ret[0].append(x(t[i]))
            ret[1].append(y(t[i]))

        return jnp.asarray(ret)
