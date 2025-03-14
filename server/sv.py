import socket
import json
import time
import random
import threading
import subprocess
import sys

ADDR = "0.0.0.0"
PORT = 8000
MAX_PLAYERS = 10
MSG_SIZE = 1073741824

# 서버 소켓 설정
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(MAX_PLAYERS)

players = {}

def generate_id(player_list: dict, max_players: int):
    # 고유 식별자 생성
    while True:
        unique_id = str(random.randint(1, max_players))
        if unique_id not in player_list:
            return unique_id

def handle_messages(identifier: str):
    client_info = players[identifier]
    conn: socket.socket = client_info["socket"]
    username = client_info["username"]

    while True:
        try:
            msg = conn.recv(MSG_SIZE)
        except ConnectionResetError:
            break

        if not msg:
            break

        msg_decoded = msg.decode("utf8")

        try:
            left_bracket_index = msg_decoded.index("{")
            right_bracket_index = msg_decoded.index("}") + 1
            msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
        except ValueError:
            continue

        try:
            msg_json = json.loads(msg_decoded)
        except Exception as e:
            print(e)
            continue

        print(f"플레이어 {username} (ID: {identifier})로부터 메시지 수신")

        if msg_json["object"] == "player":
            players[identifier]["position"] = msg_json["position"]
            players[identifier]["rotation"] = msg_json["rotation"]
            players[identifier]["health"] = msg_json["health"]

        # 다른 플레이어에게 플레이어 이동 정보 전달
        for player_id in players:
            if player_id != identifier:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.sendall(msg_decoded.encode("utf8"))
                except OSError:
                    pass

    # 다른 플레이어에게 플레이어 퇴장 정보 전달
    for player_id in players:
        if player_id != identifier:
            player_info = players[player_id]
            player_conn: socket.socket = player_info["socket"]
            try:
                player_conn.send(json.dumps({"id": identifier, "object": "player", "joined": False, "left": True}).encode("utf8"))
            except OSError:
                pass

    print(f"플레이어 {username} (ID: {identifier})가 게임에서 나갔습니다...")
    del players[identifier]
    conn.close()

def main():
    print("서버가 시작되었습니다. 새로운 연결을 기다리는 중...")

    while True:
        try:
            # 새로운 연결을 수락하고 고유 ID를 할당
            conn, addr = s.accept()
            new_id = generate_id(players, MAX_PLAYERS)
            conn.send(new_id.encode("utf8"))
            username = conn.recv(MSG_SIZE).decode("utf8")
            new_player_info = {"socket": conn, "username": username, "position": (500, 1, 500), "rotation": 0, "health": 100}

            # 기존 플레이어들에게 새로운 플레이어 정보 전달
            for player_id in players:
                if player_id != new_id:
                    player_info = players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.send(json.dumps({
                            "id": new_id,
                            "object": "player",
                            "username": new_player_info["username"],
                            "position": new_player_info["position"],
                            "health": new_player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                    except OSError:
                        pass

            # 새로운 플레이어에게 기존 플레이어 정보 전달
            for player_id in players:
                if player_id != new_id:
                    player_info = players[player_id]
                    try:
                        conn.send(json.dumps({
                            "id": player_id,
                            "object": "player",
                            "username": player_info["username"],
                            "position": player_info["position"],
                            "health": player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                        time.sleep(0.1)
                    except OSError:
                        pass

            # 새로운 플레이어를 players 목록에 추가하여 다른 플레이어로부터 메시지 수신 가능하게 함
            players[new_id] = new_player_info

            # 클라이언트로부터 메시지를 수신하기 위한 스레드 시작
            msg_thread = threading.Thread(target=handle_messages, args=(new_id,), daemon=True)
            msg_thread.start()

            print(f"새로운 연결: {addr}, 할당된 ID: {new_id}...")

        except Exception as e:
            print(f"오류 발생: {e}")
            subprocess.Popen(['python', './server.py'])
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print("종료 중")
        s.close()
