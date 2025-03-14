import ursina
from other import Other

class Damage(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float, x_direction: float, network, damage: int = 20, slave=False):
        speed = 35
        dir_rad = ursina.math.radians(direction)
        x_dir_rad = ursina.math.radians(x_direction)

        self.velocity = ursina.Vec3(
            ursina.math.sin(dir_rad) * ursina.math.cos(x_dir_rad),
            ursina.math.sin(x_dir_rad),
            ursina.math.cos(dir_rad) * ursina.math.cos(x_dir_rad)
        ) * speed

        super().__init__(
            position=position + self.velocity / speed,
            model="sphere",
            collider="box",
            scale=0.2
        )

        self.damage = damage
        self.direction = direction
        self.x_direction = x_direction
        self.slave = slave
        self.network = network

    def update(self):
        self.position += self.velocity * ursina.time.dt
        hit_info = self.intersects()

        if hit_info.hit:
            if not self.slave:
                for entity in hit_info.entities:
                    if isinstance(entity, Other):
                        entity.health -= self.damage
                        self.network.send_health(entity)

            ursina.destroy(self)
