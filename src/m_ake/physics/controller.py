import m_ake as mk
import m_ake.logic.event as event
from m_ake.physics import Actor, Walkable
import pygame as pg
from enum import Enum

import logging
logger = logging.getLogger("m_ake")

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

class Camera_controller (Actor):
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


class Space_controller (Actor):
    """
    Controller for sidescrolling zero-G environments
    """
    States = Enum("States", [
        ("INERTIAL", 0),
        ("GROUNDED", 1),
    ])
    def __init__ (self, radius=16, **kwargs):
        params = {
            "name": "Miku",
            "pos": pg.Vector2(0, 0),
            "vel": pg.Vector2(0, 0),
            "theta": 0.0,
            "omega": 0.0,
        }
        for kw in params.keys():
            try:
                params[kw] = kwargs[kw]
            except KeyError:
                pass
        self.radius = radius
        super().__init__(**params)
        # Sanitize vectors
        self.pos = pg.Vector2(self.pos)
        self.vel = pg.Vector2(self.vel)
        self.face = False
        self.__norm = -90.0

        self.timeout = 0
        self.switch_state(None)()
        self.run(False)()
        self.target_vel = pg.Vector2(0, 0)
        self.k = 0.5

        self.collider = mk.physics.collision.Circle_collider(self, radius)

        f = 3.0
        self.__press = {
        self.States.INERTIAL: {
            },
        self.States.GROUNDED: {
            pg.K_a: self.walk(pg.Vector2(-1.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(1.0, 0.0)),
            pg.K_SPACE: self.jump(pg.Vector2(0, 120)),
            },
        }
        self.__hold = {
        self.States.INERTIAL: {
            },
        self.States.GROUNDED: {
            pg.K_LSHIFT: self.run(True),
            pg.K_a: self.walk(pg.Vector2(-1.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(1.0, 0.0)),
            },
        }
        self.__release = {
        self.States.INERTIAL: {
            },
        self.States.GROUNDED: {
            pg.K_LSHIFT: self.run(False),
            pg.K_a: self.walk(pg.Vector2(0.0, 0.0)),
            pg.K_d: self.walk(pg.Vector2(0.0, 0.0)),
            },
        }

    def bind_press (self, key, action):
        self.__press[self.States.GROUNDED][key] = action
        self.__press[self.States.INERTIAL][key] = action
    
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
            self.state = self.States.GROUNDED
            self.vel = pg.Vector2(0, 0)
            self.walk(pg.Vector2(0.0, 0.0))()
            self.run(False)()
            if self.manager is not None:
                self.manager.ignore(self, path)
        else:
            self.state = self.States.INERTIAL
            self.timeout = 1
            if self.manager is not None:
                self.manager.check(self, self.path)
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
        if self.state == self.States.GROUNDED:
            self.target_vel = self.speed * val
            if self.target_vel.x < 0:
                self.face = True
            if self.target_vel.x > 0:
                self.face = False

    @command
    def jump (self, imp):
        if self.state == self.States.GROUNDED:
            self.omega = self.path.omega
            imp = imp.rotate(self.theta)
            tangent = self.path.get_tangent(self)
            vel = self.vel.rotate(self.theta)
            self.vel = vel + imp + tangent
            self.path.detach(self)
            self.switch_state()()

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

    def update (self, dt):
        if self.state == self.States.INERTIAL:
            self.__update_inertial(dt)
        else:
            self.__update_grounded(dt)

    def __update_inertial (self, dt):
        self.pos += dt * self.vel
        self.theta += dt * self.omega
        for sprite, offset in self.sprites:
            sprite.update(dt, pos=self.pos+offset, theta=self.theta,
                          face=self.face, coll=False)

    def __update_grounded (self, dt):
        vel_inc = self.k * (self.target_vel - self.vel)
        self.vel += 0.5*vel_inc
        self.vel += 0.5*vel_inc

        self.path.move(self, dt * self.vel.x)
        for sprite, offset in self.sprites:
            sprite.update(dt, pos=self.pos+offset, theta=self.theta,
                          face=self.face, vel=self.vel, coll=True)


