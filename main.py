from ursina import *
import os
import subprocess
import sys
global mainttf
mainttf = os.path.join("source", "Giants-Regular.ttf")
class LogInApp(Entity):
    def __init__(self):
        super().__init__()
        self.name_input = InputField(y=0.1, scale=(1.0, 0.1))
        self.submit_button = Button(text='Submit', font=mainttf, position=(0, 0), scale=(0.2, 0.05))
        self.greeting_text = Text('', font=mainttf, y=0.5)
        
        self.submit_button.on_click = self.submit_name
        self.name_input.on_submit = self.submit_name

        self.load_saved_name()

    def load_saved_name(self):
        if os.path.exists('./info.txt'):
            with open('./info.txt', 'r') as file:
                saved_name = file.read()
                if saved_name:
                    self.greeting_text.text = f'{saved_name} 환영합니다!'
                    self.hide()
                    main_app_instance.show()

    def submit_name(self):
        entered_name = self.name_input.text
        if entered_name:
            self.greeting_text.text = f'{entered_name} 환영합니다!'
            self.hide()
            main_app_instance.show()
            with open('./info.txt', 'w') as file:
                file.write(entered_name)

        subprocess.Popen(['python', './main.py'])
        sys.exit()


    def hide(self):
        self.name_input.disable()
        self.submit_button.disable()
        self.greeting_text.disable()

class MainApp(Entity):
    def __init__(self):
        super().__init__()

        self.init_window()

        try:
            with open('./info.txt', 'r') as file:
                player_name = file.read()
                print("미리 세팅됨 닉네임:", player_name)
            self.floating_text = Text(text = f"{player_name} 환영합니다!", font=mainttf, position = (0, 0.4), origin = (0, 0), scale = 2)
        except FileNotFoundError:
            print("파일을 찾을수 없습니다. / 경로 오류")

        main_button_texture = load_texture('mainbtn.png')
        main_button_texture.filtering = None
        main_logo = load_texture('logo.png')
        self.logo = Entity(parent = self, model='quad', texture = main_logo, scale = (6, 6), position = (0, 0.7))

        self.start_button = Button(parent = self, model='quad', text = 'Start', font=mainttf, color = color.rgb(128, 128, 128), texture = main_button_texture, scale = (2.5, 0.9), position = (0, -2))

        setting_button_texture = load_texture('settingbtn.png')
        self.setting_button = Button(parent = self, texture = setting_button_texture, scale = (0.5, 0.5), position = (-6.5, 3.5))

        self.init_events()

        self.hide()

    def init_window(self):
        window.color = color.rgb(128,128,128)
        window.fps_counter.visible = False
        window.entity_counter.visible = False
        window.collider_counter.visible = False
        window.exit_button.visible = False
        window.borderless = False
        window.title = "U"

    def init_events(self):
        self.start_button.on_click = self.on_start_button_click
        self.setting_button.on_click = self.on_setting_button_click

    def on_start_button_click(self):
        print("시작 버튼이 클릭되었습니다!")
        subprocess.Popen(['python', './game/main.py'])
        sys.exit()

    def on_setting_button_click(self):
        print("세팅 버튼이 클릭되었습니다!")
        main_app_instance.disable()
        setting_app_instance.setting_show()
        setting_app_instance.enable()

class SettingApp(Entity):
    def __init__(self):
        super().__init__()

        self.init_window()

        exit_button_texture = load_texture('settingbtn.png')
        self.exit_button = Button(parent=self, texture=exit_button_texture, scale=(0.5, 0.5), position=(-6.5, 3.5))
        self.exit_button.on_click = self.on_exit_button_click

        # self.setup_sliders()
        self.setup_name_input()
        self.setup_submit_button()

        self.setting_hide()

    def init_window(self):
        window.fps_counter.visible = False # ursina 기본값 FIX / fps 수치 비활성화
        window.entity_counter.visible = False # ursina 기본값 FIX / 엔티티 개수 수치 비활성화
        window.collider_counter.visible = False # ursina 기본값 FIX / 물체 개수 수치 비활성화
        window.exit_button.visible = False # ursina 기본값 FIX / 기본 세팅 종료 버튼 비활성화
        application.development_mode = False # ursina 기본값 FIX / 개발자 모드 비활성화
        window.title = "U" # ursina 기본값 FIX / 창 제목 변경 # ? 영향을 미치지 못함 

    def on_exit_button_click(self):
        print("세팅 나가기 버튼이 클릭되었습니다!")
        self.setting_hide()
        self.disable()
        main_app_instance.enable()

    # ? 발전 가능성 : 더 많은 세팅 (슬라이더를 이용한)

    # def setup_sliders(self):
    #     self.setup_brightness_slider()
    #     self.setup_sensitivity_slider()

    # def setup_brightness_slider(self):  # ? 반투명한 이미지 레이어 사용
    #     self.brightness_slider_ent = Slider(min=0, max=1, default=0.8, height=0.05, text='Brightness:',
    #                                            dynamic=False, radius=0.025, bar_color=color.black66)
    #     self.brightness_slider_ent.position = (-0.25, 0, 0)
    #     self.brightness_slider_ent.bar_color = color.dark_gray

    # def setup_sensitivity_slider(self): # ? FirstPersonController.mouse_sensitivity 이용 / 기본값 Vec2(40, 40)
    #     self.sensitivity_slider_ent = Slider(min=0, max=1, default=0.5, height=0.05, text='Sensitivity:',
    #                                             dynamic=False, radius=0.025, bar_color=color.black66)
    #     self.sensitivity_slider_ent.position = (-0.25, -0.2, 0)
    #     self.sensitivity_slider_ent.bar_color = color.dark_gray

    def setup_name_input(self):
        self.name_input = InputField(position = (-0.1, 0.2), scale=(0.7, 0.1))
        self.name_input_text = Text(text='', font=mainttf, y=0.5)

    def submit_name_change(self):
        new_name = self.name_input.text
        if new_name:
            with open('./info.txt', 'w') as file:
                file.write(new_name)

        subprocess.Popen(['python', './main.py'])
        sys.exit()

    def setup_submit_button(self):
        self.submit_button = Button(text='Restart', color=color.dark_gray, position=(0.4, 0.2), scale=(0.2, 0.1))
        self.submit_button.on_click = self.submit_name_change

    def setting_show(self):
        # self.brightness_slider_ent.enable()
        # self.sensitivity_slider_ent.enable()
        self.name_input.enable()
        self.name_input_text.enable()
        self.submit_button.enable()

    def setting_hide(self):
        # if self.brightness_slider_ent:
        #     self.brightness_slider_ent.disable()
        # if self.sensitivity_slider_ent:
        #     self.sensitivity_slider_ent.disable()
        if self.name_input:
            self.name_input.disable()
        if self.name_input_text:
            self.name_input_text.disable()
        if self.submit_button:
            self.submit_button.disable()


if __name__ == "__main__":
    app = Ursina()
    
    main_app_instance = MainApp()
    
    login_app = LogInApp()

    setting_app_instance = SettingApp()
    setting_app_instance.disable()
    
    app.run()
