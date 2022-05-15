from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
from mctools import QUERYClient
import bmemcached


# pip install python-binary-memcached

@dataclass
class _CONFIG:
    hostname: str = "127.0.0.1"
    port: int = None


@dataclass
class MinecraftConfig(_CONFIG):
    query_port: int = 25565
    rcon_port: int = 25575
    port: int = 25565


#  https://kb.iweb.com/hc/es/articles/230268328-C%C3%B3mo-proteger-su-servidor-del-servicio-de-Memcached

@dataclass
class MemcachedConfig(_CONFIG):
    port: int = 11211
    username: str = None
    password: str = None

    def __hash__(self) -> dict:
        asdict(self)


@dataclass
class QueryFullStats:
    motd: str = ''
    gametype: str = ''
    game_id: str = ''
    version: str = ''
    plugins: str = ''
    map: str = ''
    numplayers: str = ''
    maxplayers: str = ''
    hostport: str = ''
    hostip: str = ''
    players: list = ''
    last_insert: datetime = None
    connected: bool = ''

    def __post_init__(self):
        if not self.players: self.players = []

        self.motd = self.motd.replace("\x1b[0m", '')

        new_player_list = []
        for player in self.players:
            new_player_list.append(player.replace("\x1b[0m", ''))
        self.players = new_player_list

    def __hash__(self) -> dict:
        return asdict(self)

    def __iter__(self):
        print(f">>> {asdict(self)}")
        for attr, value in self.__hash__().items():
            value="zzzzS"
            yield attr, value


class Config():
    pass
