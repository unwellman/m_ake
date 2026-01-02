import pygame as pg
import m_ake as mk
import logging
logger = logging.getLogger("m_ake")

class Physics (object):
    """
    Prototype physics manager
    """
    def __init__ (self):
        # The exact structure of this data will be very important
        self.actors = []
        self.coll_list = set()

    def register (self, actor):
        for b in self.actors:
            self.coll_list.add((actor, b))
        self.actors.append(actor)
        actor.manager = self

    def ignore (self, a, b):
        """
        Ignore collisions between two actors
        """
        self.coll_list.discard((a, b))
        self.coll_list.discard((b, a))

    def check (self, a, b):
        self.coll_list.add((a, b))

    def check_collision (self):
        """
        Brute-force check every (unordered) pair of actors.
        Executes n(n-1)/2 checks.
        """
        collisions = []
        for a, b in self.coll_list:
            coll = a.collision(b)
            if coll:
                coll.add_info("a", a)
                coll.add_info("b", b)
                collisions.append(coll)
        return collisions

    def handle_collision (self, collisions):
        for collision in collisions:
            a = collision["a"]
            b = collision["b"]
            if isinstance(a, mk.physics.Walkable):
                a.set_zero(b, collision)
                b.switch_state(a)()
            elif isinstance (b, mk.physics.Walkable):
                b.set_zero(a, collision)
                a.switch_state(b)()

    def update (self, dt):
        collisions = self.check_collision()
        self.handle_collision(collisions)
        for actor in self.actors:
            actor.update(dt)

