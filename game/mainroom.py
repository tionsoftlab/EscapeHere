import os
import ursina
import random

class Floor:
    def __init__(self):
        self.floor_entity = ursina.Entity(
            position=(0, 0, 0),
            scale=(120, 1, 120),  
            model="cube",
            texture=os.path.join("assets", "floor.png"),
            collider="box",
        )
        self.floor_entity.texture.filtering = None


class Wall(ursina.Entity):
    def __init__(self, position, scale):
        super().__init__(
            position=position,
            scale=scale,
            model="cube",
            texture=os.path.join("assets", "wall3.png"),
            origin_y=0,
        )
        self.texture.filtering = None
        self.collider = ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


class Wall_in:
    def __init__(self):
        Wall(ursina.Vec3(-43, 2, 40), (26, 8, 1))
        Wall(ursina.Vec3(-30.5, 2, 50), (1, 8, 15))
        Wall(ursina.Vec3(-43, 2, -40), (26, 8, 1))
        Wall(ursina.Vec3(-30.5, 2, -50), (1, 8, 15))
        Wall(ursina.Vec3(30.5, 2, -50), (1, 8, 15))
        Wall(ursina.Vec3(43, 2, -40), (26, 8, 1))
        Wall(ursina.Vec3(43, 2, 40), (26, 8, 1))
        Wall(ursina.Vec3(30.5, 2, 50), (1, 8, 15))


class Wall_random:
    def __init__(self):
        for i in range(1, 10):
            random.seed(i)
            Wall(
                ursina.Vec3(random.randint(-50, 50), 3, random.randint(-50, 50)),
                (15, 10, 1),
            )

        for i in range(1, 10):
            random.seed(i)
            Wall(
                ursina.Vec3(random.randint(-50, 50), 3, random.randint(-50, 50)),
                (1, 10, 15),
            )


class Wall1(ursina.Entity):
    def __init__(self, position, scale):
        super().__init__(
            position=position,
            scale=scale,
            model="cube",
            texture=os.path.join("assets", "wall2.png"),
            origin_y=0,
        )
        self.texture.filtering = None
        self.collider = ursina.BoxCollider(self, size=ursina.Vec3(1, 2, 1))


class Wall_out:
    def __init__(self):
        Wall1(ursina.Vec3(0, 3, 60), (120, 10, 1))
        Wall1(ursina.Vec3(0, 3, -60), (120, 10, 1))
        Wall1(ursina.Vec3(60, 3, 0), (1, 10, 120))
        Wall1(ursina.Vec3(-60, 3, 0), (1, 10, 120))
