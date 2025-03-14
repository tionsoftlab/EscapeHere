import ursina
import os

class Other(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            collider="box",
            texture = os.path.join("assets", "task.png"),
            model=os.path.join("assets", "player.obj"),
            scale= ursina.Vec3(0.4, 0.4, 0.4)
        )
        self.name_tag = ursina.Text(
            font= os.path.join("assets", "Giants-Inline.ttf"),
            parent=self,
            text=username,
            position=ursina.Vec3(0, 5.2, 0),
            scale=ursina.Vec2(6, 4),
            billboard=True,
            origin=ursina.Vec2(0, 0),
            color = ursina.color.yellow
        )

        self.health = 100
        self.id = identifier
        self.username = username
        self.game_end = False
        self.pos = ursina.Vec2(0, 0)
        self.size = ursina.Vec2(1.8, 1)

    def update(self):
        try:
            hp = self.health
            if self.world_position.x >= 1000:
                self.game_end = True
                self.world_position = ursina.Vec3(300, 0.4, 300)
                self.failpopup = ursina.Entity(
                    parent=ursina.camera.ui,
                    model="quad",
                    position=self.pos,
                    scale=self.size,
                    texture=os.path.join("assets", "fail.png"),
                )
            if hp <= 0:
                self.health = 100
                self.world_position = ursina.Vec3(300, 0.4, 300)
            color_saturation = 1 - self.health / 100
        except AttributeError:
            self.health = 100
            color_saturation = 1 - self.health / 100
        self.color = ursina.color.color(0, color_saturation, 1)

