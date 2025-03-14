import os
from ursina import *

class escape(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(57, 0.3, 4),
            texture = os.path.join("assets", "task.png"),
            model=os.path.join("assets", "escape.glb"),
            scale=Vec3(1, 1, 1),
            collider='box',
        )
        self.pos = Vec2(0, 0)
        self.size = Vec2(1.8, 1)

    def create_popup(self):
        self.popup = Entity(
            parent=camera.ui,
            model="quad",
            position=self.pos,
            scale=self.size,
            texture=os.path.join("assets", "escape.png"),
        )
        destroy(self.popup, delay=20)

