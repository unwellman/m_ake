import m_ake as mk
import pygame as pg

class Pause (mk.State):
    pass

def command (func):
    """
    Utility decorator for easily binding commands to keys

    Instead of the command running when called, it returns a void
    callable that runs the command, allowing the command to be delayed
    or repeated.
    """
    def ret (*args, **kwargs):
        def callback ():
            func(*args, **kwargs)
        return callback
    return ret

class Controller (mk.event.Event_handler):
    """
    Start with a typical platformer character controller
    """
    def __init__ (self):
        types = None
        self.__pos = pg.Vector2(0, 0)
        self.__vel = pg.Vector2(0, 0)
        self.__acc = pg.Vector2(0, 0)
        self.__theta = 0.0
        self.__omega = 0.0
        self.__face = False

        self.run(False)()
        self.move(pg.Vector2(0.0, 0.0))()

        f = 3.0
        self.__press = {
            pg.K_a: self.move(pg.Vector2(-1.0, 0)),
            pg.K_d: self.move(pg.Vector2(1.0, 0)),
            pg.K_s: self.stop(),
            pg.K_RIGHT: self.rotate(f),
            pg.K_LEFT: self.rotate(-f),
            pg.K_RSHIFT: self.stop(),
            pg.K_LSHIFT: self.run(True),
        }
        self.__hold = {
            pg.K_a: self.move(pg.Vector2(-1.0, 0)),
            pg.K_d: self.move(pg.Vector2(1.0, 0)),
            pg.K_RIGHT: self.rotate(-f),
            pg.K_LEFT: self.rotate(f),
        }
        self.__release = {
            pg.K_LSHIFT: self.run(False),
            pg.K_a: self.move(pg.Vector2(0.0, 0.0)),
            pg.K_d: self.move(pg.Vector2(0.0, 0.0)),
        }

    @command
    def reposition (self, pos):
        self.__pos = pos

    @command
    def move (self, inc):
        self.__target = self.__speed * inc
        if inc.x < 0:
            self.__face = True
        elif inc.x > 0:
            self.__face = False

    @command
    def run (self, cond):
        if cond:
            self.__speed = 90
            self.__k = 12
        else:
            self.__speed = 36
            self.__k = 8

    @command
    def rotate (self, inc):
        self.__omega += inc

    @command
    def stop (self):
        self.__omega = 0.0
        self.__vel = pg.Vector2(0, 0)
        self.__theta = 0.0

    @command
    def collide (self, direction):
        pass

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
        self.__acc = self.__k*(self.__target - self.__vel)

        # Use an easy first-order correction to forward Euler
        self.__vel += 0.5 * dt * self.__acc
        self.__pos += dt * self.__vel
        self.__vel += 0.5 * dt * self.__acc

        self.__theta += dt * self.__omega
        sprite.update(dt, pos=self.__pos, theta=self.__theta,
                      face=self.__face, vel=self.__vel)

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
        miku = mk.gfx.Sprite()
        miku.load_config("res/programmer_assets/migu.yml")
        self.miku = miku
        self.screen.register(miku)
        self.screen.clear_color = pg.Color(48, 48, 48)

        self.controller = Controller()
        self.controller.reposition(pg.Vector2(240, 135))()

    def loop (self, dt):
        self.controller.poll()
        self.controller.update(self.miku, dt)
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

