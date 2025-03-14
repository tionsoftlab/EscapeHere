import ursina
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time

class Player(FirstPersonController):
    def __init__(self, position: ursina.Vec3):
        super().__init__(
            position=position,
            jump_height=2.5,
            jump_duration=0.4,
            origin_y=-2,
            collider="box",
            speed=7
        )
        self.cursor.color = ursina.color.rgb(255, 0, 0, 122)

        
        self.gun = ursina.Entity(
            parent=ursina.camera.ui,
            position=ursina.Vec2(0.6, -0.45),
            scale=ursina.Vec3(0.2, 0.2, 1),
            rotation=ursina.Vec3(-20, -20, -5),
            model="cube",
            color=ursina.color.rgb(166, 247, 253)
        )

        self.healthbar_pos = ursina.Vec2(0, 0.45)
        self.healthbar_size = ursina.Vec2(0.8, 0.04)
        self.healthbar_bg = ursina.Entity(
            parent=ursina.camera.ui,
            model="quad",
            color=ursina.color.rgb(255, 0, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        self.healthbar = ursina.Entity(
            parent=ursina.camera.ui,
            model="quad",
            color=ursina.color.rgb(0, 255, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        self.is_cooldown = False
        self.cooldown_timer = 1.0
        self.death_timer = None
        self.is_dead = False
        self.counter_text = None
        self.health = 100

    def reset_cooldown(self):
        self.is_cooldown = False

    def death(self):
        self.death_timer = time.time()
        self.death_timer_duration = 10
        self.world_position = ursina.Vec3(0, 1, 0)

        self.counter_text = ursina.Text(
            text=str(self.death_timer_duration),
            origin=ursina.Vec2(0, 0),
            scale=3
        )

    def update(self):
        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.health = 0
            self.death()

        if self.is_dead:
            self.world_position = ursina.Vec3(200, 50, 200)
            elapsed_time = int(time.time() - self.death_timer)
            remaining_time = self.death_timer_duration - elapsed_time
            self.speed = 0

            if remaining_time > 0:
                self.counter_text.text = str(remaining_time)
                if elapsed_time >= 10:
                    self.is_dead = False
                    self.origin_y = -2,
                    self.speed = 7
                    self.health = 100  
                    self.world_position = ursina.Vec3(0, 1, 0)
                    self.counter_text.text = ""
            else:
                self.is_dead = False
                self.counter_text.text = ""
                self.origin_y = -2
                self.world_position = ursina.Vec3(0, 1, 0)
                self.speed = 7
                self.health = 100  

        self.healthbar.scale_x = self.health / 100 * self.healthbar_size.x
        super().update()
