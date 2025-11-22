import m_ake as mk
import pygame as pg
import math
import logging
logger = logging.getLogger("m_ake")

class Station_sprite (mk.gfx.sprite.Drawable):
    def __init__ (self, rad):
        super().__init__(size=(2*rad + 4, 2*rad + 4))
        self.rad = rad

    def draw (self, angle):
        self.fill(pg.Color(0, 0, 0, 0))
        pg.draw.circle(self, pg.Color(255, 255, 255),
                pg.Vector2(self.rad + 2, self.rad + 2), self.rad, width=2)

        center = pg.Vector2(self.rad + 2, self.rad + 2)
        point = pg.Vector2(self.rad, 0).rotate(-angle)
        pg.draw.circle(self, pg.Color(255, 0, 0),
                center + point.rotate(0), 2, width=0)
        pg.draw.circle(self, pg.Color(255, 255, 0),
                center + point.rotate(60), 2, width=0)
        pg.draw.circle(self, pg.Color(0, 255, 0),
                center + point.rotate(120), 2, width=0)
        pg.draw.circle(self, pg.Color(0, 255, 255),
                center + point.rotate(180), 2, width=0)
        pg.draw.circle(self, pg.Color(0, 0, 255),
                center + point.rotate(240), 2, width=0)
        pg.draw.circle(self, pg.Color(255, 0, 255),
                center + point.rotate(300), 2, width=0)

    def get_blit_args (self, camera):
        self.draw(camera.theta - self.theta)
        a = camera.radius

        left_top = camera.pos.rotate(-camera.theta) \
            + (self.rad + 2 - a, self.rad + 2 - a)
        rect = pg.FRect(left_top, (2*a, 2*a))
        center_0 = pg.Vector2(rect.center)
        rect = rect.clip(self.get_rect())
        center_1 = pg.Vector2(rect.center)
        offset = (center_1 - center_0).rotate(camera.theta)
        ret = self.subsurface(rect)
        return ret, camera.pos + offset

class Station (mk.State):
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
        Load sprite and animations
        """
        if Station.instance:
            return
        self.__screen = mk.gfx.Screen((480, 270))
        miku = mk.gfx.Animated()
        miku_fp = mk.get_path("res/programmer_assets/migu.yml")
        miku.load_config(miku_fp)
        self.miku = miku
        self.screen.register(miku)

        rad = 2000
        acc = 80
        self.station = Station_sprite(rad)
        self.screen.register(self.station)
        self.screen.clear_color = pg.Color(24, 24, 24)
        self.camera = Camera_controller(self.miku)

        params = {
            "radius": rad,
            "name": "space_station",
            "pos": pg.Vector2(0, 0),
            "vel": pg.Vector2(0, 0),
            "theta": 0.0,
            "omega": math.sqrt(acc/rad)*180/math.pi,
        }
        self.path = mk.logic.shapes.Circle_Path(**params)
        self.controller = Controller()
        self.controller.pos = pg.Vector2(0, -rad*0.9)
        self.rotate_camera = mk.logic.event.State_bool(True)
        self.controller.bind_press(pg.K_RSHIFT, self.rotate_camera(False))
        self.controller.bind_press(pg.K_RETURN, self.rotate_camera(True))

    def loop (self, dt):
        if self.controller.state == Controller.States.INERTIAL:
            if self.path.collision(self.controller):
                self.controller.switch_state(self.path)()
        self.controller.poll()

        self.path.update(self.station, dt)
        self.controller.update(self.miku, dt)
        self.camera.update(self.screen, dt, self.rotate_camera)
        self.screen.draw()

    def __repr__ (self):
        return "platformer"

    def pause (self, *args, **kwargs):
        pass

    def resume (self, *args, **kwargs):
        kwargs["window"].bind_screen(self.__screen)

    @property
    def screen (self):
        return self.__screen


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

override = pg.event.custom_type()

from enum import Enum

class Camera_controller (mk.logic.actor.Actor):
    """
    Trying different ways of operating the camera
    """
    def __init__ (self, actor, **kwargs):
        """
        actor: the actor that the camera should track
        """
        super().__init__(**kwargs)
        self.actor = actor
        self.k = 0.80

    def update (self, screen, dt, rotate_camera=True):
        if rotate_camera:
            screen.reposition(self.actor.pos, self.actor.theta)
        else:
            screen.reposition(self.actor.pos)

    def collision (self, other):
        return False

class Controller (mk.logic.actor.Actor):
    """
    A foray into multiple inheritance?
    """
    States = Enum("States", [
        ("INERTIAL", 0),
        ("GROUNDED", 1),
    ])
    def __init__ (self):
        params = {
            "name": "Miku",
            "pos": pg.Vector2(0, 0),
            "vel": pg.Vector2(0, -60),
            "theta": 0.0,
            "omega": 0.0,
        }
        self.radius = 16
        super().__init__(**params)
        self.face = False
        self.__norm = -90.0

        self.timeout = 0
        self.switch_state(None)()
        self.run(False)()
        self.target_vel = pg.Vector2(0, 0)
        self.offset = 0.0
        self.k = 0.5

        f = 3.0
        self.__press = {
        Controller.States.INERTIAL: {
            },
        Controller.States.GROUNDED: {
            pg.K_a: self.walk(pg.Vector2(-1.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(1.0, 0.0)),
            pg.K_SPACE: self.jump(pg.Vector2(0, 120)),
            },
        }
        self.__hold = {
        Controller.States.INERTIAL: {
            },
        Controller.States.GROUNDED: {
            pg.K_LSHIFT: self.run(True),
            pg.K_a: self.walk(pg.Vector2(-1.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(1.0, 0.0)),
            },
        }
        self.__release = {
        Controller.States.INERTIAL: {
            },
        Controller.States.GROUNDED: {
            pg.K_LSHIFT: self.run(False),
            pg.K_a: self.walk(pg.Vector2(0.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(0.0, 0.0)),
            },
        }

    def bind_press (self, key, action):
        self.__press[Controller.States.GROUNDED][key] = action
        self.__press[Controller.States.INERTIAL][key] = action
    
    @property
    def norm (self):
        return self.__norm

    @norm.setter
    def norm (self, val):
        self.__norm = val
        self.theta = val + 90

    @command
    def switch_state (self, path=None):
        if self.timeout > 0:
            return
        if path is not None:
            self.state = Controller.States.GROUNDED
            path.set_zero(self)
            self.vel = pg.Vector2(0, 0)
            self.offset = 0.0
            self.walk(pg.Vector2(0.0, 0.0))()
            self.run(False)()
        else:
            self.state = Controller.States.INERTIAL
            self.timeout = 1
        self.path = path

    @command
    def reposition (self, pos):
        self.pos = pos

    @command
    def run (self, cond):
        if cond:
            self.speed = 90
        else:
            self.speed = 36

    @command
    def walk (self, val):
        if self.state == Controller.States.GROUNDED:
            self.target_vel = self.speed * val
            if self.target_vel.x < 0:
                self.face = True
            if self.target_vel.x > 0:
                self.face = False

    @command
    def jump (self, imp):
        if self.state == Controller.States.GROUNDED:
            self.omega = self.path.omega
            imp = imp.rotate(self.theta)
            tangent = self.path.get_tangent(self)
            vel = self.vel.rotate(self.theta)
            self.vel = vel + imp + tangent
            self.path.detach(self)
            self.switch_state()()

    def collision (self, other):
        return False

    def poll (self):
        self.timeout -= 1
        pressed = pg.key.get_just_pressed()
        for k, v in self.__press[self.state].items():
            if pressed[k]:
                v()
        held = pg.key.get_pressed()
        for k, v in self.__hold[self.state].items():
            if held[k]:
                v()
        released = pg.key.get_just_released()
        for k, v in self.__release[self.state].items():
            if released[k]:
                v()

    def update (self, sprite, dt):
        if self.state == Controller.States.INERTIAL:
            self.__update_inertial(sprite, dt)
        else:
            self.__update_grounded(sprite, dt)

    def __update_inertial (self, sprite, dt):
        self.pos += dt * self.vel
        self.theta += dt * self.omega
        sprite.update(dt, pos=self.pos, theta=self.theta,
                      face=self.face, coll=False)

    def __update_grounded (self, sprite, dt):
        vel_inc = self.k * (self.target_vel - self.vel)
        self.vel += 0.5*vel_inc
        self.offset += dt * self.vel.x
        self.vel += 0.5*vel_inc

        self.path.move(self, self.offset)
        sprite.update(dt, pos=self.pos, theta=self.theta,
                      face=self.face, vel=self.vel, coll=True)


