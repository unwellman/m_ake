import pygame as pg
import m_ake as mk

class Actor (object):
    """
    Class encompassing 2-D rigid bodies

    Attributes:
        mass: physical mass used for momentum transfers
        inertia: moment of inertia about the axis normal to the screen
        pos: pg.Vector2 castable position
        vel: linear velocity
        acc: linear acceleration
        theta: angular position
        omega: angular velocity
        alpha: angular acceleration
    """
    defaults = {
        "mass": 1,
        "inertia": 1,
        "pos": (0, 0),
        "vel": (0, 0),
        "acc": (0, 0),
        "theta": 0,
        "omega": 0,
        "alpha": 0,
        }
    def __init__ (self, *args, **kwargs):
        """
        Initialize the actor with kwargs

        Implementation details:
            Moment of inertia is computed as mass*inertia, so that changing
            an object's mass alone will create an intuitive change in its
            rotational inertia.

            Passing float("inf") as a mass will result in an immovable object,
            as expected. Passing a nonpositive number raises an exception.
        """
        self.__dict__.update(Actor.defaults)
        keys = Actor.defaults.keys()
        for key, val in kwargs.items():
            if key in keys:
                self.__dict__[key] = val
        if self.mass <= float(0):
            raise ValueError("Mass must be positive or inf")
        self.inertia = self.mass * self.inertia

        # List of tuple (sprite, offset)
        self.__sprites = []

        # List of tuple (collider, offset)
        self.__colliders = []

    def register_sprite (self, spt, offset, collision=False):
        """
        Set a sprite to update relative to the position of the actor

        Parameters:
            spt: mk.gfx.Sprite object
            offset: Castable to pg.Vector2
            collision: Whether to add the sprite as a collider
        """
        self.__sprites.append((spt, offset))
        if collision:
            self.__colliders.append((spt, offset))

class Physics (object):
    """
    Class for logically managing a set of physically interacting 2D objects
    """
    def __init__ (self):
        pass

    def fast_update (self):
        """
        Change object parameters to handle fast input changes
        """
        pass

    def tick (self, dt):
        """
        Tick the whole simulation forward in time by dt and handle persistent
        inputs

        Parameters:
            dt: float seconds since last tick
        """
        pass

