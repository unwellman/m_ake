import m_ake as mk
import pygame as pg
import numpy as np
import abc
import enum
import functools

import logging
logger = logging.getLogger("m_ake")

class Collision (object):
    """
    Container for properties of a collision

    Attributes:
        colliders: tuple of the two colliders involved
        pos: pg.Vector2 position of the collision
    """
    def __init__ (self, a, b, pos):
        self.colliders = (a, b)
        self.pos = pg.Vector2(pos)
        self.info = {}

    def __bool__ (self):
        return True

    def add_info (self, key, val):
        self.info[key] = val

    def __getitem__ (self, key):
        return self.info[key]

@functools.total_ordering
class Collision_priority (enum.Enum):
    """
    Enumeration of unique types of collision primitives.

    A subclass of Collider must implement a collision checking function
    for each subclass with a lower priority value.
    """

    POINT = 1
    CIRCLE = 2
    LINE = 3
    RECTANGLE = 4
    PARAMETRIC = 5
    POLYGON = 6
    GROUP = 999
    def __lt__ (self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        raise TypeError("Collision_priority comparison is only supported within the Enum")


class Collider (abc.ABC):
    """
    Abstract class for colliders with collision-checking properties.

    A subclass of Collider must implement a collision checking function
    for each subclass with a lower priority value.

    Attributes:
        solvers: dict of methods indexed by Collision_priority
        priority: Member of enum Collision_priority
    """

    solvers = {}
    priority = None

    @property
    @abc.abstractmethod
    def pos (self):
        return self.actor.pos

    @property
    @abc.abstractmethod
    def theta (self):
        return self.actor.theta

    def check (self, other):
        if other.priority > self.priority:
            return other.check(self)
        return self.solvers[other.priority](other)


class Group_collider (Collider):
    """
    Collider representing a collection of primitives
    """
    priority = Collision_priority.GROUP
    def __init__ (self, colliders):
        self.colliders = []
        for collider in colliders:
            self.register(collider)
        self.solvers = {
            Collision_priority.POINT: self.check_single,
            Collision_priority.CIRCLE: self.check_single,
            Collision_priority.LINE: self.check_single,
            Collision_priority.RECTANGLE: self.check_single,
            Collision_priority.PARAMETRIC: self.check_single,
            Collision_priority.POLYGON: self.check_single,
            Collision_priority.GROUP: self.check_group,
        }

    def check_single (self, other):
        for collider in self.colliders:
            coll = collider.check(other)
            if coll:
                return coll
        return False

    def check_group (self, other):
        for i in self.colliders:
            for j in other.colliders:
                coll = i.check(j)
                if coll:
                    return coll
        return False

    def __iter__ (self):
        return self.colliders

    def register (self, collider):
        # Expand any groups that are fed in
        if isinstance(collider, Group_collider):
            for obj in collider:
                self.register(obj)
        else:
            self.colliders.append(collider)


class Position_collider (Collider, metaclass=abc.ABCMeta):
    """
    Abstract base class for colliders with a position and offset relative to
    an actor.

    Properties:
        actor: A physics.Actor to bind to
        offset: An offset vector in the actor's local coordinates
        offset_theta: A rotational offset from the actor's angle
    """

    priority = None
    solvers = {}
    actor = None
    offset = pg.Vector2(0, 0)
    offset_theta = 0.0
    
    @property
    def pos (self):
        return self.actor.pos + self.offset.rotate(self.actor.theta)

    @property
    def theta (self):
        return self.actor.theta + self.offset_theta

class Point_collider (Position_collider):
    """
    Point-particle; only collides when exactly on top of another
    """
    priority = Collision_priority.POINT
    def __init__ (self, actor):
        self.actor = actor
        self.solvers = {
            Collision_priority.POINT: self.check_point,
        }
    
    def check_point (self, other):
        if self.pos == other.pos:
            return Collision(self, other, self.pos)
        return False

class Circle_collider (Position_collider):
    """
    Circle; compares radius with distance from another
    """
    priority = Collision_priority.CIRCLE
    def __init__ (self, actor, radius):
        self.actor = actor
        self.radius = radius
        self.r_sq = radius ** 2
        self.solvers = {
            Collision_priority.POINT: self.check_point,
            Collision_priority.CIRCLE: self.check_circle,
        }

    def check_point (self, other):
        if (self.pos - other.pos).magnitude_squared() <= self.r_sq:
            return Collision(self, other, other.pos)
        return False

    def check_circle (self, other):
        radii = self.radius + other.radius
        if (self.pos - other.pos).magnitude_squared <= radii ** 2:
            diff = (other.pos - self.pos).normalize()
            pos = self.pos + other.pos + (self.radius - other.radius) * diff
            return Collision(self, other, pos/2)
        return False


class Line_collider (Position_collider):
    """
    Line; collides when intersecting with another
    """
    priority = Collision_priority.LINE
    def __init__ (self, actor, vector):
        """
        Changing the offset and offset_theta attributes allows for any line
        segment to be made
        """
        self.actor = actor
        self.vector = pg.Vector2(vector)


class Rectangle_collider (Position_collider):
    """
    Rectangle; collides when overlapping another
    """
    priority = Collision_priority.RECTANGLE
    def __init__ (self, actor, width, height):
        """
        Similarly to line segments, offset and offset_theta can be used for
        setting the position of the rectangle
        """
        self.actor = actor

class Parametric_collider (Position_collider):
    """
    Parametric curve in line segments; collides when intersecting another.
    """
    priority = Collision_priority.PARAMETRIC
    def __init__ (self, actor):
        assert isinstance(actor, mk.physics.shapes.Parametric)
        self.actor = actor
        
        # Makes a bunch of references to actor; prevents parametric colliders
        # from differing in shape to what is drawn on screen
        self.points = actor.points
        self.radii = actor.radii
        self.angles = actor.angles
        self.mats = actor.mats

        self.solvers = {
            Collision_priority.POINT: None,
            Collision_priority.CIRCLE: self.check_circle,
            Collision_priority.LINE: None,
            Collision_priority.RECTANGLE: None,
        }

    def make_collision (self, other, sol, coll):
        mask = np.where(coll, sol, float("nan"))
        idx = np.nanargmin(np.square(mask[1]))
        st = sol[:, idx] * self.radii[idx]
        logger.debug(f"{idx}, {st}")
        local = pg.Vector2(st).rotate(self.angles[idx])
        local += self.points[:, idx]
        local = local.rotate(self.theta)
        pos = self.pos + local
        ret = Collision(self, other, pos)
        ret.add_info("idx", idx)
        ret.add_info("st", st)
        return ret

    def check_circle (self, other):
        """
        """
        _, n = self.points.shape
        # Note that pts is a view of self.points in-place, not a new array
        pts = self.points.swapaxes(0, 1).reshape((n, 2, 1))[0:n-1, :, :]
        # Compute other.pos in local coordinates
        diff = (self.pos - other.pos).rotate(-self.theta)
        # See scratch paper
        sol = self.mats @ (pts + np.array([[diff.x], [diff.y]]))
        sol = sol.reshape((n-1, 2)).swapaxes(0, 1)
        sol /= np.square(self.radii)
        orthogonal = np.square(sol[1])
        parallel = sol[0]
        norms = (other.radius / self.radii) ** 2
        not_skew = np.logical_and(np.less_equal(parallel, 1.1),
                                  np.less_equal(-0.1, parallel))
        coll = np.logical_and(not_skew, np.less_equal(orthogonal, norms))
        logger.debug(f"{sol[:,10]}")
        if np.nonzero(coll)[0].size > 0:
            return self.make_collision(other, sol, coll)
        return False


class Polygon_collider (Collider):
    """
    (Convex) polygon; collides when overlapping another
    """
    priority = Collision_priority.POLYGON

