import m_ake as mk
import pygame as pg

class Pause (mk.State):
    pass

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
        Load sprite and animations
        """
        if Platform.instance:
            return
        self.__screen = mk.gfx.Screen((480, 270))
        miku = mk.gfx.Sprite()
        miku_fp = mk.get_path("res/programmer_assets/migu.yml")
        miku.load_config(miku_fp)
        self.miku = miku
        self.screen.register(miku)
        self.screen.clear_color = pg.Color(48, 48, 48)

        self.controller = mk.logic.Platformer_controller()
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
        kwargs["window"].bind_screen(self.__screen)

    @property
    def screen (self):
        return self.__screen

