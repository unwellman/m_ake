import pygame as pg
import m_ake as mk

class Window:
    def __init__ (self, *args, **kwargs):
        f = mk.config.pixel_factor
        self.params = {
            "title": "m ake",
            "size": (f*mk.config.width, f*mk.config.height),
            "position": pg.WINDOWPOS_CENTERED,
            "resizable": True,
        }
        self.window = pg.Window(**self.params)
        self.surface = self.window.get_surface()
        self.screen = None
        try:
            self.clock = kwargs["clock"]
            self.font = pg.font.SysFont("Arial", 18)
        except KeyError:
            self.clock = None

    def fps_counter (self):
        if not self.clock:
            return
        text = f"{self.clock.get_fps():.2f}"
        surf = self.font.render(text, 1, pg.Color("WHITE"))
        self.surface.blit(surf, (0, 0))

    def bind_screen (self, screen):
        self.screen = screen

    def __call__ (self):
        self.surface.fill("black")
        self.screen.upscale(self.surface)
        self.fps_counter()
        self.window.flip()

