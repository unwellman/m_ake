import m_ake as mk
import pygame as pg
import numpy as np

class Parametric (mk.gfx.sprite.Sprite):
    def __init__ (self, material, points, **kwargs):
        """
        Parameters:
            material: callable that returns a surface given an angle
            points (ndarray (2, n)): points returned by parametric importer
        """
        super().__init__(**kwargs)
        self.material = material
        self.points = points
        self.get_centers_angles()

    def get_blit_args (self, camera):
        for i in range(len(self.centers)):
            point = pg.Vector2(self.centers[i])
            cond = (camera.radius + self.material.scale)**2
            if (point + self.pos - camera.pos).magnitude_squared() > cond:
                continue
            theta = self.angles[i]
            surf = self.material(theta)
            pos = point.rotate(self.theta) + self.pos
            yield surf, pos

    def get_centers_angles (self):
        """
        """
        r, c = self.points.shape
        centers = np.zeros((r, c-1))
        centers += self.points[:, 0:c-1]
        centers += self.points[:, 1:c]
        centers /= 2
        self.centers = centers.swapaxes(0, 1)
        tmp = pg.Vector2(0, 0)
        angles = []
        for i in range(c-1):
            tmp.x = self.points[0, i+1] - self.points[0, i]
            tmp.y = self.points[1, i+1] - self.points[1, i]
            angles.append(tmp.angle)
        self.angles = np.array(angles)

