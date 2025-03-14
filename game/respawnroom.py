import os
import ursina


class RespawnRoom:
    def __init__(self):
        self.floor_entity = ursina.Entity(
            position=(200, 50, 200),
            scale=(3, 1, 3),  
            model="cube",
            texture=os.path.join("assets", "wall.png"),
            collider="box"
        )
        self.floor_entity.texture.filtering = None