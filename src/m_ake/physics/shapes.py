import pygame as pg
import numpy as np
import m_ake as mk
from m_ake.physics import Walkable, Actor
import math
import logging
logger = logging.getLogger("m_ake")

class Parametric (Actor):
    def __init__ (self, points, loop=False, collision=True, **kwargs):
        """
        Initialize superclass and some methods

        Note that points are in local coordinates
        """
        super().__init__(**kwargs)
        self.points = points
        self.loop = loop
        self.precompute()
        if collision:
            self.collider = mk.physics.collision.Parametric_collider(self)

    def precompute (self):
        """
        The construction of the solution matrices is incorrect.
        """
        _, n = self.points.shape
        radii = []
        angles = []
        mats = []
        for i in range(n - 1):
            vec = self.points[:,i+1] - self.points[:,i]
            radii.append(np.linalg.norm(vec))
            angles.append(pg.Vector2(vec).angle)
            # This construction is actually going to make me kill myself
            # There is literally no reason that this should be difficult
            mat = [[ self.points[0,i] - self.points[0,i+1],
                     self.points[1,i] - self.points[1,i+1] ],
                   [ self.points[1,i+1] - self.points[1,i],
                     self.points[0,i] - self.points[0,i+1] ]]
            mat = np.asarray(mat)
            mats.append(mat)

        self.radii = np.asarray(radii)
        self.mats = np.asarray(mats)
        self.angles = angles


class Parametric_path (Parametric, Walkable):
    def __init__ (self, points, loop, **kwargs):
        """
        Warning: Actor gets initialized twice
        """
        Parametric.__init__(self, points, loop, **kwargs)
        Walkable.__init__(self, **kwargs)

    def set_zero (self, actor, collision):
        """
        """
        idx = collision["idx"]
        st = collision["st"]
        st[1] = actor.radius if st[1] >= 0 else -actor.radius
        self.positions[actor] = (idx, st)
        logger.debug(f"Added {actor} at {idx} {st}, angle {self.angles[idx]}")

    def move (self, actor, offset):
        idx, st = self.positions[actor]
        if st[1] < 0:
            offset = -offset
        if offset < 0:
            offset = -offset
            conv = -1
        else:
            conv = 1
        remaining = (1 + conv)/2 * self.radii[idx] - conv*st[0]
        while offset > remaining:
            offset -= remaining
            idx += conv
            if self.loop:
                idx %= len(self.radii)
            elif idx not in range(len(self.radii)):
                raise NotImplementedError("")
                self.detach(actor)
            remaining = self.radii[idx]
            st[0] = (1 - conv)/2 * self.radii[idx]
        st[0] += conv*offset
        self.positions[actor] = (idx, st)

    def __compute_rel_pos (self, idx, st):
        rel = pg.Vector2(self.points[:, idx])
        segment = pg.Vector2(st).rotate(self.angles[idx])
        return (rel + segment).rotate(self.theta)

    def update (self, dt):
        for actor, val in self.positions.items():
            idx, st = val
            actor.pos = self.pos + self.__compute_rel_pos(idx, st)
            actor.theta = self.angles[idx] + self.theta
            if st[1] < 0:
                actor.theta += 180

    def get_tangent (self, actor):
        try:
            idx, st = self.positions[actor]
        except KeyError:
            return None
        rel_pos = self.__compute_rel_pos(idx, st)
        return self.vel + self.omega * math.pi / 180 \
                * rel_pos.rotate(90)

