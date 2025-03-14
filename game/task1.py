import os
from ursina import *

class Task1(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(-21, 0.3, 22),
            texture = os.path.join("assets", "box.png"),
            model=os.path.join("assets", "box.glb"),
            scale=Vec3(0.5, 0.5, 0.5),
            collider='box',
        )

        self.z1 = 999999
        self.x1 = 999999
        self.c1 = 999999
        self.v1 = 999999
        self.pos = Vec2(0, 0)
        self.size = Vec2(1.0, 0.7)
        self.done = False


        self.z_pressed = False
        self.x_pressed = False
        self.c_pressed = False
        self.v_pressed = False

    def create_popup(self):
        self.popup = Entity(
            parent=camera.ui,
            model="quad",
            position=self.pos,
            scale=self.size,
            texture=os.path.join("assets", "task1.png"),
        )
        destroy(self.popup, delay=20)
        self.z1 = 3
        self.x1 = 4
        self.c1 = 5
        self.v1 = 2

    def update(self):
        if not self.z_pressed and held_keys['z']:
            self.z1 -= 1
            self.z_pressed = True
        elif not held_keys['z']:
            self.z_pressed = False

        if not self.x_pressed and held_keys['x']:
            self.x1 -= 1
            self.x_pressed = True
        elif not held_keys['x']:
            self.x_pressed = False

        if not self.c_pressed and held_keys['c']:
            self.c1 -= 1
            self.c_pressed = True
        elif not held_keys['c']:
            self.c_pressed = False

        if not self.v_pressed and held_keys['v']:
            self.v1 -= 1
            self.v_pressed = True
        elif not held_keys['v']:
            self.v_pressed = False

        if self.z1 <= 0 and self.x1 <= 0 and self.c1 <= 0 and self.v1 <= 0:
            self.done = True
            destroy(self.popup)
            destroy(self)
