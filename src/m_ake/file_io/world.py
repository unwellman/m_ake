import numpy as np
import yaml

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
    def parametric (cls, dct):
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
        n = 2*data["arc_sample"] # ensure even for Simpson's rule
        rng = data["parameter"]
        mi, ma = min(rng), max(rng)
        if data["cycle"]:
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
        sample_length = data["scale"]
        logger.debug(f"World spline {dct["id"]} sampling {sample_length}")

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
        # Ensure that the last point is included
        ret[0].append(x[-1])
        ret[1].append(y[-1])

        return np.asarray(ret)
