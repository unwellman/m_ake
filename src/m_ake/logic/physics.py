import pygame as pg

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

