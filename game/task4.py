import os
from ursina import *

class Task4(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(-16, 0.3, 28),
            texture = os.path.join("assets", "box.png"),
            model=os.path.join("assets", "box.glb"),
            scale=Vec3(0.5, 0.5, 0.5),
            collider='box',
        )

        self.c1 = 999999
        self.pos = Vec2(0, 0)
        self.size = Vec2(1.0, 0.7)
        self.done = False

        self.c_pressed = False

    def create_popup(self):
        self.popup = Entity(
            parent=camera.ui,
            model="quad",
            position=self.pos,
            scale=self.size,
            texture=os.path.join("assets", "task4.png"),
        )
        destroy(self.popup, delay=20)
        self.c1 = 12

    def update(self):
        if not self.c_pressed and held_keys['c']:
            self.c1 -= 1
            self.c_pressed = True
        elif not held_keys['c']:
            self.c_pressed = False

        if self.c1 <= 0:
            self.done = True
            destroy(self.popup)
            destroy(self)
