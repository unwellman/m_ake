import m_ake as mk
import pygame as pg

class Pause (mk.State):
    pass

class Controller (mk.event.Event_handler):
    """
    Absolute bare-minimum character controller simulator
    """
    def __init__ (self):
        types = None
        self.__pos = pg.Vector2(0, 0)
        self.__vel = pg.Vector2(0, 0)
        self.__acc = pg.Vector2(0, 0)
        self.__theta = 0.0
        self.__omega = 0.0

        f = 3.0
        self.__press = {
            pg.K_w: self.accel(f*pg.Vector2( 0, -1), change=True),
            pg.K_a: self.accel(f*pg.Vector2(-1,  0), change=True),
            pg.K_s: self.accel(f*pg.Vector2( 0,  1), change=True),
            pg.K_d: self.accel(f*pg.Vector2( 1,  0), change=True),
            pg.K_RIGHT: self.rotate(f),
            pg.K_LEFT: self.rotate(-f),
        }
        self.__hold = {
            pg.K_w: self.accel(f*pg.Vector2( 0, -1)),
            pg.K_a: self.accel(f*pg.Vector2(-1,  0)),
            pg.K_s: self.accel(f*pg.Vector2( 0,  1)),
            pg.K_d: self.accel(f*pg.Vector2( 1,  0)),
            pg.K_RIGHT: self.rotate(-f),
            pg.K_LEFT: self.rotate(f),
        }
        self.__release = {
            
        }

    def accel (self, inc, change=False):
        def func ():
            self.__vel += inc
            self.__accel = inc
            if change:
                self.__accel = pg.Vector2(0, 0)
        return func

    def rotate (self, inc):
        def func ():
            self.__omega += inc
        return func

    def collide (self, direction):
        def func ():
            pass
        return func

    def poll (self):
        pressed = pg.key.get_just_pressed()
        for k, v in self.__press.items():
            if pressed[k]:
                v()
        held = pg.key.get_pressed()
        for k, v in self.__hold.items():
            if held[k]:
                v()
        released = pg.key.get_just_released()
        for k, v in self.__release.items():
            if released[k]:
                v()

    def update (self, sprite, dt):
        self.__pos += dt*self.__vel
        self.__theta += dt*self.__omega
        sprite.update(dt, pos=self.__pos, theta=self.__theta)

    def inc_pos_callback (self, inc):
        return lambda: self.__pos 

class Platform (mk.State):
    instance = None # Singleton
    def __new__ (cls, *args, **kwargs):
        """
        Singleton behavior
        """
        if cls.instance:
            return cls.instance
        return super().__new__(cls, *args, **kwargs)

    def __init__ (self, *args, **kwargs):
        """
        Load Lucy
        """
        if Platform.instance:
            return
        self.__screen = mk.gfx.Screen((480, 270))
        lucy = mk.gfx.Sprite()
        lucy.load_sheet("res/programmer_assets/lucy.png")
        lucy.queue_animation("idle_E", loop=True)
        self.lucy = lucy
        self.screen.register(lucy)
        self.screen.clear_color = pg.Color(48, 48, 48)

        self.controller = Controller()

    def loop (self, dt):
        self.controller.poll()
        self.controller.update(self.lucy, dt)
        self.screen.draw()

    def __str__ (self):
        return "platformer"

    def pause (self, *args, **kwargs):
        pass

    def resume (self, *args, **kwargs):
        kwargs['window'].bind_screen(self.__screen)

    @property
    def screen (self):
        return self.__screen

