import pygame as pg
import m_ake as mk
from m_ake.logic.actor import Walkable
import math
import logging
logger = logging.getLogger("m_ake")

class Circle_Path (Walkable):
    def __init__ (self, radius, **kwargs):
        """
        Incl radius

        Note that superclass args must be passed by keyword
        """
        super().__init__(**kwargs)
        self.radius = radius

    def set_zero (self, actor, direction=1.0):
        """
        Parameters:
            float direction: -1.0 or 1.0 for outside vs inside
        """
        rel_pos = actor.pos - self.pos
        try:
            rel_pos.scale_to_length(self.radius - direction * actor.radius)
        except ValueError:
            pass
        actor.norm = rel_pos.angle
        self.positions[actor] = (rel_pos, self.theta, actor.norm)

    def move (self, actor, offset):
        """
        """
        rel_pos, rel_theta, norm = self.positions[actor]
        offset = offset / self.radius * 180 / math.pi
        rel_theta -= offset
        rel_pos = rel_pos.rotate(self.theta - rel_theta)
        actor.pos = rel_pos + self.pos
        actor.theta = self.theta - rel_theta + norm + 90

    def get_tangent (self, actor):
        try:
            rel_pos, rel_theta, norm = self.positions[actor]
        except KeyError:
            return None
        return self.omega * math.pi / 180 \
                * rel_pos.rotate(self.theta - rel_theta + 90)

    def update (self, sprite, dt):
        self.pos += dt * self.vel
        self.theta += dt*self.omega
        if self.theta > 360:
            self.theta -= 360
        sprite.pos = self.pos
        sprite.theta = self.theta

    def collision (self, actor):
        # In principle, check object types and default to circle
        return self.__collision_circle(actor)

    def __collision_circle (self, actor):
        x = (actor.pos - self.pos).magnitude_squared()
        if (self.radius - actor.radius)**2 <= x < self.radius**2:
            return 1 # Inside collision
        if self.radius**2 < x <= (self.radius + actor.radius)**2:
            return -1 # Outside collision
        return 0 # No collision (or exactly centered on the edge)

