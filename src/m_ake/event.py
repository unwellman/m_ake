import pygame as pg

class State_variable (object):
    def __init__ (self, val):
        self.val = val

    def 


class Event_handler (object):
    def __init__ (self):
        pass

    def __call__ (self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                

