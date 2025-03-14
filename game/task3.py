import os
from ursina import *

class Task3(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(56, 0.3, 55),
            texture = os.path.join("assets", "box.png"),
            model=os.path.join("assets", "box.glb"),
            scale=Vec3(0.5, 0.5, 0.5),
            collider='box',
        )

        self.z1 = 999999
        self.pos = Vec2(0, 0)
        self.size = Vec2(1.0, 0.7)
        self.done = False

        self.z_pressed = False

    def create_popup(self):
        self.popup = Entity(
            parent=camera.ui,
            model="quad",
            position=self.pos,
            scale=self.size,
            texture=os.path.join("assets", "task3.png"),
        )
        destroy(self.popup, delay=20)
        self.z1 = 12

    def update(self):
        if not self.z_pressed and held_keys['z']:
            self.z1 -= 1
            self.z_pressed = True
        elif not held_keys['z']:
            self.z_pressed = False

        if self.z1 <= 0:
            self.done = True
            destroy(self.popup)
            destroy(self)
