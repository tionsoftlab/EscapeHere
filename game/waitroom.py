import os
import ursina

class Wait_Floor:
    def __init__(self):
        self.floor_entity = ursina.Entity(
            position=(500, 0, 500),
            scale=(30, 1, 30),
            model="cube",
            texture=os.path.join("assets", "floor.png"),
            collider="box"
        )
        self.floor_entity.texture.filtering = None

class Wall(ursina.Entity):
    def __init__(self, position, scale):
        super().__init__(
            position=position,
            scale=scale,
            model="cube",
            texture=os.path.join("assets", "wall2.png"),
            origin_y=0
        )
        self.texture.filtering = None
        self.collider = ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


class Wait_Wall_out:
    def __init__(self):
        Wall(ursina.Vec3(500, 3, 515), (30, 10, 1))
        Wall(ursina.Vec3(500, 3, 485), (30, 10, 1))
        Wall(ursina.Vec3(515, 3, 500), (1, 10, 30))
        Wall(ursina.Vec3(485, 3, 500), (1, 10, 30))