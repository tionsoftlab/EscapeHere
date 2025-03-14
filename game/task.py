import os
from ursina import *
import ursina

class Task(ursina.Entity):
    def __init__(self):
        super().__init__(
            
            position = ursina.Vec3(5, 2, 0),
            scale= ursina.Vec3(0.4, 0.4, 0.4),
            collider='box',
            
            texture=os.path.join("assets", "task.png"),
            model=os.path.join("assets", "task.obj"),
        )

        self.popup = None
        self.popup_open = False

    def on_task_click(self):
        self.create_popup()

    def create_popup(self):
        self.popup = Panel(
            z=1,
            scale=(1.0, 0.7),
            origin=(0, 0),
            background=True,
            draggable=True,
        )
        self.popup_open = True

        text = Text(parent=self.popup, text="Hello", scale=1.5)

    def close_key(self):
        if held_keys['x']:
            print("팝업 닫기 버튼 클릭됨")
            if self.popup:
                destroy(self.popup)
                self.popup_open = False
# import os
# from ursina import *

# class Task:
#     def __init__(self):
#         self.task_entity = Entity(
#             position=(0, 2, 0),
#             scale=(2, 1, 2),
#             collider='box',
#             model="cube",
#             texture=os.path.join("assets", "task.png")
#         )
#         self.task_entity.texture.filtering = None

#         self.task_entity.on_click = self.on_task_click
#         self.popup = None
#         self.popup_open = False

#     def on_task_click(self):
#         self.create_popup()

#     def create_popup(self):
#         self.popup = Panel(
#             z=1,
#             scale=(1.0, 0.7),
#             origin=(0, 0),
#             background=True,
#             draggable=True,
#         )
#         self.popup_open = True

#         text = Text(parent=self.popup, text="Hello", scale=1.5)

#     def close_key(self):
#         if held_keys['x']:
#             print("팝업 닫기 버튼 클릭됨")
#             if self.popup:
#                 destroy(self.popup)
#                 self.popup_open = False