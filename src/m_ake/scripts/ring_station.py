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
        return [(ret, camera.pos + offset)]

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
        self.camera = mk.logic.Camera_controller(self.miku)

        params = {
            "radius": rad,
            "name": "space_station",
            "pos": pg.Vector2(0, 0),
            "vel": pg.Vector2(0, 0),
            "theta": 0.0,
            "omega": math.sqrt(acc/rad)*180/math.pi,
        }
        self.path = mk.logic.shapes.Circle_Path(**params)
        self.controller = mk.logic.Space_controller()
        self.controller.pos = pg.Vector2(0, -rad*0.9)
        self.controller.vel = pg.Vector2(0, -60)
        self.controller.register(self.miku)
        self.rotate_camera = mk.logic.event.State_bool(True)
        self.controller.bind_press(pg.K_RSHIFT, self.rotate_camera(False))
        self.controller.bind_press(pg.K_RETURN, self.rotate_camera(True))

    def loop (self, dt):
        if self.controller.state == mk.logic.Space_controller.States.INERTIAL:
            if self.path.collision(self.controller):
                self.controller.switch_state(self.path)()
        self.controller.poll()

        self.path.update(self.station, dt)
        self.controller.update(dt)
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

