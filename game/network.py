import socket
import json

from player import Player
from other import Other
from damage import Damage

class Network:
    """
    Args:
        server_addr (str): 서버의 IPv4 주소
        server_port (int): 서버가 실행 중인 포트
        username (str): 이 클라이언트의 플레이어 사용자 이름
    """

    def __init__(self, server_addr: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.username = username
        self.recv_size = 2048
        self.id = 0

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):
        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def receive_info(self):
        try:
            msg = self.client.recv(self.recv_size)
        except socket.error as e:
            print(e)

        if not msg:
            return None

        msg_decoded = msg.decode("utf8")

        left_bracket_index = msg_decoded.index("{")
        right_bracket_index = msg_decoded.index("}") + 1
        msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]

        msg_json = json.loads(msg_decoded)

        return msg_json

    def send_player(self, player: Player):
        player_info = {
            "object": "player",
            "id": self.id,
            "position": (player.world_x, player.world_y, player.world_z),
            "rotation": player.rotation_y,
            "health": player.health,
            "joined": False,
            "left": False
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
        except socket.error as e:
            print(e)

    def send_damage(self, damage: Damage):
        damage_info = {
            "object": "damage",
            "position": (damage.world_x, damage.world_y, damage.world_z),
            "damage": damage.damage,
            "direction": damage.direction,
            "x_direction": damage.x_direction
        }

        damage_info_encoded = json.dumps(damage_info).encode("utf8")

        try:
            self.client.send(damage_info_encoded)
        except socket.error as e:
            print(e)

    def send_health(self, player: Other):
        health_info = {
            "object": "health_update",
            "id": player.id,
            "health": player.health
        }

        health_info_encoded = json.dumps(health_info).encode("utf8")

        try:
            self.client.send(health_info_encoded)
        except socket.error as e:
            print(e)
