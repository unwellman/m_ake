import pygame as pg
import m_ake as mk

from abc import ABC
from abc import ABCMeta
from abc import abstractmethod

import logging
logger = logging.getLogger("m_ake")

class Actor (ABC):
    """
    Base class for in-game physical actors.

    Attributes:
        string name: representation used for hashing
        pg.Vector2 pos: world position in pixels
        pg.Vector2 vel: world velocity in pixels/sec
        float theta: angular position in degrees
        float omega: angular velocity in degrees/sec
    """
    defaults = {
        "name": "actor",
        "pos": pg.Vector2(0, 0),
        "vel": pg.Vector2(0, 0),
        "theta": 0.0,
        "omega": 0.0,
    }
    def __init__ (self, **kwargs):
        try:
            self.__collider
        except AttributeError:
            self.__collider = None
        self.__manager = None
        self.__dict__.update(Actor.defaults)
        keys = Actor.defaults.keys()
        for key, val in kwargs.items():
            if key in keys:
                self.__dict__[key] = val
        self.sprites = []

    def __repr__ (self):
        return self.name

    def register (self, sprite, offset=pg.Vector2(0, 0)):
        self.sprites.append((sprite, offset))

    @property
    def manager (self):
        """
        The Physics instance which updates this actor
        """
        return self.__manager

    @manager.setter
    def manager (self, manager):
        self.__manager = manager

    @property
    def collider (self):
        if self.__collider is None:
            raise AttributeError(f"{self} does not have a collider")
        return self.__collider

    @collider.setter
    def collider (self, collider):
        self.__collider = collider

    def collision (self, other):
        """
        """
        a = self.__collider
        b = other._Actor__collider
        if (a is None) or (b is None):
            return False
        return a.check(b)

class Walkable (Actor, metaclass=ABCMeta):
    """
    Represents a path that an actor can lock onto and walk along.
    """
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        self.positions = {}

    @abstractmethod
    def set_zero (self, actor):
        """
        Introduce a new actor to the surface at its current position
        """
    
    @abstractmethod
    def move (self, actor, offset):
        """
        Update the world position of actor, moved along the walkable path
        by offset pixels of arc length.
        """
    
    def detach (self, actor):
        """
        Remove the reference to the actor
        """
        try:
            self.positions.pop(actor)
        except KeyError:
            pass

