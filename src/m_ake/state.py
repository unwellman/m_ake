import pygame as pg
import m_ake as mk

class State (type):
    """
    Metaclass for game states
    """
    def __call__ (cls, *args, **kwargs):
        return super(State, cls).__call__(*args, **kwargs)

