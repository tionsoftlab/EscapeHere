"""
게임 메인 코드
# ! 이 주석이 빨강색으로 보이지 않는다면, 확장 Better Comments를 VSCode에 설치 하시는 것을 권고 드립니다. / 미설치 시 코드가 어지럽게 보일 수 있습니다.
# ! 작업시에 사용하였던 모든 디버깅 요소는 개발이 끝난 후 반드시 삭제하십시오.
# TODO : 닉네임 / 설정 값 적용
# TODO : 플레이어 스탠바이 여부에 따른 게임시작 or 시작 x 구현
# TODO : Task 인게임 미니게임 구현
# TODO : 승리 구별 및 승리화면 통합
"""

# * 필요 라이브러리 가져오기
import os
import sys
import socket
import threading
from ursina import held_keys
import ursina

# * 필요 파이썬(.py) 파일 가져오기
from network import Network  # 네트워크
from player import Player  # 플레이어 (자신)
from other import Other  # 플레이어 (다른 플레이어)
from damage import Damage  # 데미지
from task1 import Task1  # 작업1(Task)
from task2 import Task2  # 작업2(Task)
from task3 import Task3  # 작업3(Task)
from task4 import Task4  # 작업4(Task)
from task5 import Task5  # 작업5(Task)
from waitroom import Wait_Floor, Wait_Wall_out  # 대기실 벽/바닥
from start import Start  # 게임 시작 버튼
from mainroom import Floor, Wall_out, Wall_in, Wall_random  # 우주선 벽/바닥
from respawnroom import RespawnRoom  # 리스폰 바닥
from escape import Escape  # 비상탈출장치

try:
    with open('./info.txt', 'r') as file:
        player_name = file.read()
    username = player_name
except FileNotFoundError:
    print("파일을 찾을수 없습니다. / 경로 오류")

# * 서버 통신
while True:
    server_ip = "121.143.210.85"  # ? ../server/sv.py를 미리 실행 시켜둔 서버 주소
    server_port = "8000"  # ? ../server/sv.py를 미리 실행 시켜둔 서버 포트

    # * 서버 연결 오류 검증
    try:
        server_port = int(server_port)
    except ValueError:
        print("\n입력된 서버주소가 숫자가 아닙니다. 정확한 서버주소를 사용 하였는지 재 확인 바랍니다.")
        continue
    n = Network(server_ip, server_port, username)
    n.settimeout(5)
    error_occurred = False
    try:
        n.connect()
    except ConnectionRefusedError:
        print("\n연결이 끊겼습니다... 플레이어 정원이 가득 찼거나, 서버가 닫혀있을 수 있습니다.")
        error_occurred = True
    except socket.timeout:
        print("\n서버 연결에 너무 긴 시간이 소요되고 있습니다. 재시도 바랍니다.")
        error_occurred = True
    except socket.gaierror:
        print("\nIP 주소가 유효하지 않습니다. 유효한 IP 주소를 사용하여 접속 바랍니다.")
        error_occurred = True
    finally:
        n.settimeout(None)
    # * 연결 작업 종료
    if not error_occurred:
        break

# * 기본 세팅
app = ursina.Ursina()  # ursina 라이브러리 선언
ursina.window.fps_counter.visible = False  # ursina 기본값 FIX / fps 수치 비활성화
ursina.window.entity_counter.visible = False  # ursina 기본값 FIX / 엔티티 개수 수치 비활성화
ursina.window.collider_counter.visible = False  # ursina 기본값 FIX / 물체 개수 수치 비활성화
ursina.window.exit_button.visible = False  # ursina 기본값 FIX / 기본 세팅 종료 버튼 비활성화
ursina.application.development_mode = False  # ursina 기본값 FIX / 개발자 모드 비활성화
ursina.window.title = "U"  # ursina 기본값 FIX / 창 제목 변경 # ? 영향을 미치지 못함

# * 불러온 파이썬(.py) 파일 선언
# 메인 우주선
floor = Floor()  # 바닥
main_out = Wall_out()  # 외벽
main_in = Wall_in()  # 내부 벽
main_random = Wall_random()  # 내부 벽 2
task1 = Task1()  # 작업1 (Task)
task2 = Task2()  # 작업2 (Task)
task3 = Task3()  # 작업3 (Task)
task4 = Task4()  # 작업4 (Task)
task5 = Task5()  # 작업5 (Task)

# 대기실
wait_room_wall = Wait_Wall_out()  # 외벽
wait_room_floor = Wait_Floor()  # 바닥
start = Start()

# 리스폰
respawn = RespawnRoom()

# 비상 탈출 장치
escape = Escape()

# * 요소 선언
bg = ursina.Entity(
    model="sphere",
    texture=os.path.join("assets", "bg.png"),
    scale=9999,
    double_sided=True
)  # 우주 배경 설정
player = Player(ursina.Vec3(500, 1, 500))  # 플레이어 생성 및 위치 배정
pre_pos = player.world_position  # 이전 값 저장
pre_dir = player.world_rotation_y
others = []  # 외부 플레이어 선언

# * 플레이어 / 데미지 서버 통신
def receive():
    while True:
        try:
            info = n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("서버가 멈췄습니다! 재접속을 권고 드립니다.")
            sys.exit()

        if info["object"] == "player":
            other_id = info["id"]

            if info["joined"]:
                new_other = Other(ursina.Vec3(
                    *info["position"]), other_id, info["username"])
                new_other.health = info["health"]
                others.append(new_other)
                continue

            other = None

            for e in others:
                if e.id == other_id:
                    other = e
                    break

            if not other:
                continue

            if info["left"]:
                others.remove(other)
                ursina.destroy(other)
                continue

            other.world_position = ursina.Vec3(*info["position"])
            other.rotation_y = info["rotation"]

        elif info["object"] == "damage":
            b_pos = ursina.Vec3(*info["position"])
            b_dir = info["direction"]
            b_x_dir = info["x_direction"]
            b_damage = info["damage"]
            new_damage = Damage(b_pos, b_dir, b_x_dir, n, b_damage, slave=True)
            ursina.destroy(new_damage, delay=0.13)

        elif info["object"] == "health_update":
            other_id = info["id"]

            other = None

            if other_id == n.id:
                other = player
            else:
                for e in others:
                    if e.id == other_id:
                        other = e
                        break

            if not other:
                continue

            other.health = info["health"]

# * 실시간 업데이트
def update():
    if player.health > 0:
        # ! print(player.world_position) # 디버그용 좌표 확인
        global pre_pos, pre_dir

        if pre_pos != player.world_position or pre_dir != player.world_rotation_y:
            n.send_player(player)

        pre_pos = player.world_position
        pre_dir = player.world_rotation_y

        
        if task1:
            distance_to_object = (
                player.world_position - task1.position).length()
            if distance_to_object <= 3:
                if held_keys['t']:
                    task1.create_popup()
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="t를 눌러\n작업을 시작해보세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True)
                    ursina.destroy(helptext, delay=0.1)
        if task2:
            distance_to_object = (
                player.world_position - task2.position).length()
            if distance_to_object <= 3:
                if held_keys['t']:
                    task2.create_popup()
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="t를 눌러\n작업을 시작해보세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True)
                    ursina.destroy(helptext, delay=0.1)
        if task3:
            distance_to_object = (
                player.world_position - task3.position).length()
            if distance_to_object <= 3:
                if held_keys['t']:
                    task3.create_popup()
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="t를 눌러\n작업을 시작해보세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True)
                    ursina.destroy(helptext, delay=0.1)
        if task4:
            distance_to_object = (
                player.world_position - task4.position).length()
            if distance_to_object <= 3:
                if held_keys['t']:
                    task4.create_popup()
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="t를 눌러\n작업을 시작해보세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True, delay=0.1)
                    ursina.destroy(helptext, delay=0.2)
        if task5:
            distance_to_object = (
                player.world_position - task5.position).length()
            if distance_to_object <= 3:
                if held_keys['t']:
                    task5.create_popup()
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="t를 눌러\n작업을 시작해보세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True, delay=0.1)
                    ursina.destroy(helptext, delay=0.2)
        def count_false_variables(q, w, e, r, t):
            false_count = 0
            for variable in [q, w, e, r, t]:
                if not variable:
                    false_count += 1
            return false_count
        false_count = count_false_variables(
                task1.done, task2.done, task3.done, task4.done, task5.done)

        if escape:
            distance_to_object = (
                player.world_position - escape.position).length()
            if distance_to_object <= 3:
                if held_keys['e']:
                    if false_count <= 0:
                        escape.create_escape_popup()
                        player.world_position = ursina.Vec3(1500, 3, 1500)

                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="작업을 모두 완료했다면,\ne를 눌러\n비상탈출장치를 사용하세요!",
                        scale=ursina.Vec2(1.5, 1.5),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True, delay=0.1)
                    ursina.destroy(helptext, delay=0.2)

        if start:
            distance_to_object = (
                player.world_position - start.position).length()
            if distance_to_object <= 3:
                if held_keys['e']:
                    player.health = 0
                else:
                    helptext = ursina.Text(
                        font=os.path.join("assets", "Giants-Regular.ttf"),
                        text="플레이할 인원이 모두 참석 했다면,\n다른 플레이어와 동시에\ne를 눌러 게임에 시작하세요!",
                        scale=ursina.Vec2(2, 2),
                        position=ursina.Vec2(-0.8, -0.3),
                        background=True, delay=0.1)
                    ursina.destroy(helptext, delay=0.2)

        # ! 작업 갯수 화면 업데이트
        if (
            player.world_position.x <= 60
            and player.world_position.x >= -60
            and player.world_position.z >= -60
            and player.world_position.z <= 60
        ):
            tasktext = ursina.Text(
                font=os.path.join("assets", "Giants-Regular.ttf"),
                text="남은 작업 갯수 : " + str(false_count),
                scale=ursina.Vec2(2, 2),
                position=ursina.Vec2(-0.2, -0.38),
                background=True)
            ursina.destroy(tasktext, delay=0.1)
        # # ! Shift 키를 누르면 플레이어 이동 속도 증가 (개발용도 / 맵뚫 요소)
        # move_speed = 5 if held_keys['shift'] else 0
        # if held_keys['f']:  # ! D 키를 눌렀을 때 플레이어 목숨 10 감소 (개발용도)
        #     player.health -= 10
        # player.position += player.forward * (ursina.time.dt * move_speed)

# * 키 입력 감지
def input(key):
    if key == "q":
        sys.exit()
    # if key == "r":
    #     player.world_position = ursina.Vec3(0, 3, 0)
    if key == "right mouse down" and player.health > 0 and not player.is_cooldown:
        if (
            player.world_position.x <= 60
            and player.world_position.x >= -60
            and player.world_position.z >= -60
            and player.world_position.z <= 60
        ):
            player.is_cooldown = True
            ursina.invoke(player.reset_cooldown, delay=1) 
            b_pos = player.position + ursina.Vec3(0, 2, 0)
            damage = Damage(b_pos, player.world_rotation_y, -
                            player.camera_pivot.world_rotation_x, n)
            n.send_damage(damage)
            ursina.destroy(damage, delay=0.3)


# * 실행
def main():
    msg_thread = threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    app.run()


if __name__ == "__main__":
    main()
