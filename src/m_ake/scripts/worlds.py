import pygame as pg
import m_ake as mk

import logging
logger = logging.getLogger("m_ake")

class Miku_world (mk.State):
    def __init__ (self, *args, **kwargs):
        self.__screen = mk.gfx.Screen((480, 270))
        world_fp = mk.get_path("res/programmer_assets/world_0.yml")
        self.world = mk.file_io.World_importer(world_fp)
        self.physics = mk.physics.Physics()
        self.init_actors_sprites()
        self.conditions()

    def conditions (self):
        actor, sprite = self.world.geometry["floor"]
        actor.omega = 10

    def init_actors_sprites (self):
        self.physics.register(self.world.controller)
        self.screen.register(self.world.player)
        for key, val in self.world.geometry.items():
            actor, sprite = val
            self.physics.register(actor)
            self.screen.register(sprite)

    def __repr__ (self):
        return "miku_world"

    def loop (self, dt):
        controller = self.world.controller
        controller.poll()
        self.physics.update(dt)
        self.screen.reposition(controller.pos, controller.theta)
        self.screen.draw()
        debug = f"frame:\n\tcontroller: {self.world.controller.pos}\n\tcamera: {self.screen.camera.pos}\n\tfloor: {self.world.geometry['floor'][0].pos}"
        #logger.debug(debug)

    def pause (self, *args, **kwargs):
        pass

    def resume (self, *args, **kwargs):
        kwargs["window"].bind_screen(self.screen)

    @property
    def screen (self):
        return self.__screen

