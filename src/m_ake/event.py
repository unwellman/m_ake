import pygame as pg
import m_ake as mk

class State_bool (object):
    """
    Simple callable class for storing bools
    """
    def __init__ (self, val):
        self.__set(val)

    def __set (self, val):
        if val:
            self.val = True
        else:
            self.val = False

    def __bool__ (self):
        return self.val

    def __call__ (self, val):
        return lambda dct: self.__set(val)

class Event_handler (object):
    def __init__ (self):
        self.actions = {}

    def bind (self, event, func):
        """
        Bind a pygame event to an arbitrary function.

        Parameters:
            event: pygame event type
            func: action accepting 
        """
        if event in self.actions.keys():
            mk.logger.info(f"Bound event {event}: {self.actions[event]}"\
            "overridden with {func}")

        self.actions[event] = func

    def __call__ (self):
        for event in pg.event.get():
            try:
                self.actions[event.type](event.__dict__)
            except KeyError:
                pass

