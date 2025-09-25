import pygame as pg
import m_ake as mk

class Actor (object):
    """
    Class encompassing 2-D rigid bodies

    Attributes:
        mass: physical mass used for momentum transfers
        inertia: moment of inertia about the axis normal to the screen
        pos: center-of-mass position in world coordinates
        vel: linear velocity
        acc: linear acceleration
        theta: angular position
        omega: angular velocity
        alpha: angular acceleration
    """
    defaults = {
        "mass": 1,
        "inertia": 1,
        "elast": 0.90,
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
            raise ValueError("Mass must be positive")
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

    def check_collision (self, other):
        """
        Check if this object is colliding with another
        """
        for spt in self.__colliders:
            surf, pos = spt.get_blit_args(advance=False)
            collider = pg.mask.from_surface(surf)
            intersection = other.check_collider(collider, pos)
            if intersection:
                return intersection

        return None

    def check_collider (self, collider, pos):
        """
        Check if this object is colliding with another mask
        """
        for spt in self.__colliders:
            surf, origin = spt.get_blit_args(advance=False)
            mask = pg.mask.from_surface(surf)
            intersection = mask.overlap(collider, pos - origin)
            if intersection:
                return pg.Vector2(intersection) + origin

        return None

collision = pg.event.custom_type()

class Collision (object):
    """
    Representation of object collision events
    """
    def __init__ (self, actor1, actor2, intersection):
        """
        Get necessary properties and initialize superclass
        """
        self.properties = {
            "obj": self,
            "actors": (actor1, actor2),
            }

    def queue (self):
        """
        Place this event on the global event queue
        """
        ev = pg.event.Event(collision, self.properties)
        pg.event.post(ev)

    def solve (self, a, b, pos):
        """
        Placeholder method for expressions
        """
        E_init = 0.5 * (a.mass * a.vel.magnitude_squared() \
                + b.mass * b.vel.magnitude_squared() \
                + a.inertia * a.omega**2 + b.inertia * b.omega**2)

    def solve_point_particle (self):
        """
        Solve the collision in the point particle approximation
        """
        import math
        A = self.actor1
        B = self.actor2
        f = A.elast * B.elast
        M = A.mass
        a, b = A.vel
        p, q = A.pos
        m = B.mass
        c, d = B.vel
        r, s = B.pos

        x = ((M*a + m*a)*(q-s)**2 + (m*d + m*b)*(q-s)*(p-r) + m * (p-r) *\
            math.sqrt(-((a-c)*(q-s) - (b-d)*(p-r))**2 - f*((a-c)**2 + (b-d)**2)\
            *((p-r)**2 + (q-s)**2)))/((M+m)*((p-r)**2 + (q-s)**2))

        y = b + (x - a) * (q - s) / (p - r)

        z = (M*a + m*c - M*x)/m

        w = (M*b + m*d - M*y)/m
        A.vel = pg.Vector2(x, y)
        B.vel = pg.Vector2(z, w)

class Physics (object):
    """
    Class for logically managing a set of physically interacting 2D objects
    """
    def __init__ (self, *args, **kwargs):
        self.gravity = -1
        self.actors = [] # Eventually change this data structure

    def register (self, actor):
        """
        Register an actor with this physics system
        """
        self.actors.append(actor)

    def fast_update (self, dt):
        """
        Change object parameters to handle fast input changes
        """
        for actor in self.actors:
            pass

    def tick (self, dt):
        """
        Tick the whole simulation forward in time by dt and handle persistent
        inputs

        Parameters:
            dt: float seconds since last tick
        """
        pass

    def __collide_brute_force (self):
        """
        Check collision for every registered object
        """
        for i in range(len(self.actors)):
            a = self.actors[i]
            for j in range(len(self.actors)).pop(i):
                b = self.actors[j]
                intersection = a.check_collision(b)
                if intersection:
                    coll = Collision(a, b, intersection)
                    coll.solve_point_particle()
            

