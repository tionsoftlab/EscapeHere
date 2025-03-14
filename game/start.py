import os
from ursina import *

class Start(Entity):
    def __init__(self):
        super().__init__(
            position=Vec3(505, 0.3, 505),
            texture = os.path.join("assets", "box.png"),
            model=os.path.join("assets", "escape.glb"),
            scale=Vec3(1, 1, 1),
            collider='box',
        )
        self.pos = Vec2(0, 0)
        self.size = Vec2(1.8, 1)


