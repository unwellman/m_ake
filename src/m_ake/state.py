import pygame as pg
import m_ake as mk

import abc

# Custom event for handling state changes
state_change = pg.event.custom_type()


class State (abc.ABC):
    """
    Abstract base class for game states
    """
    @abc.abstractmethod
    def __init__ (self, *args, **kwargs):
        """
        Initialize the state, including required properties
        """
        pass

    @abc.abstractmethod
    def __repr__ (self):
        """
        Each instance should have a unique identifier for hashing
        Changed from __str__ to be more idiomatic
        """
        pass

    @abc.abstractmethod
    def loop (self, dt):
        """
        Run this state's game loop, with dt s having passed since the last frame
        """
        pass

    @abc.abstractmethod
    def pause (self, *args, **kwargs):
        """
        Prepare to suspend the game state
        """
        pass

    @abc.abstractmethod
    def resume (self, *args, **kwargs):
        """
        Prepare to resume this game state
        """
        pass

    @property
    @abc.abstractmethod
    def screen (self):
        """
        The screen object which this state will display to the main window.

        Also used to draw the game under a pause menu
        """
        pass


