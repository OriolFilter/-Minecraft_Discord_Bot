from dataclasses import dataclass, asdict
from mctools import QUERYClient
import bmemcached
from datetime import datetime


# pip install python-binary-memcached

@dataclass()
class _CONFIG:
    hostname: str = "127.0.0.1"
    port: int = None


@dataclass()
class MinecraftConfig(_CONFIG):
    query_port: int = 25565
    rcon_port: int = 25575
    port: int = 25565


#  https://kb.iweb.com/hc/es/articles/230268328-C%C3%B3mo-proteger-su-servidor-del-servicio-de-Memcached

@dataclass()
class MemcachedConfig(_CONFIG):
    port: int = 11211
    username: str = None
    password: str = None

    def __hash__(self) -> dict:
        asdict(self)


@dataclass
class QueryFullStats:
    motd: str = None
    gametype: str = None
    game_id: str = None
    version: str = None
    plugins: str = None
    map: str = None
    numplayers: str = None
    maxplayers: str = None
    hostport: str = None
    hostip: str = None
    players: list = None

    def __post_init__(self):
        if not self.players: self.players = []

        self.motd = self.motd.replace("\x1b[0m", '')

        new_player_list = []
        for player in self.players:
            new_player_list.append(player.replace("\x1b[0m", ''))
        self.players = new_player_list

    def __hash__(self) -> dict:
        return asdict(self)


class _CLI:
    __config: object

    # def _insert_config(self, config: object):
    #     self.__config = config
    #
    # def insert_config(self, config: object):
    #     self.__insert_config(config)
    #
    # def __init__(self, config=None):
    #     if config:
    #         self.insert_config(config)

    # @property
    # def config(self) -> __insert_config.__config:
    #     return self.__config


class MemcachedCli(_CLI):
    __config: MemcachedConfig

    def __init__(self, config=None):
        if config:
            self.__config = config

    # def __init__(self, config=None):
    #     print(config)
    #     self.__config = config
    #     if config:
    #         self.insert_config(config)
    # print(self.__config)

    def insert_dict(self, data: dict | QueryFullStats):
        if isinstance(data, QueryFullStats): data = dict(data.__hash__())
        memcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)

        for key, value in data.items():
            # assert key, value
            memcache_cli.set(key, value)
        memcache_cli.set("last_insert", datetime.now())

    def \
            get_from_memcached(self, key: str):
        memcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)
        return memcache_cli.get(key=key)


class MinecraftCli(_CLI):
    __config: MinecraftConfig

    def __init__(self, config=None):
        if config:
            self.__config = config

    def get_full_stats(self) -> QueryFullStats:
        print("Quering to MC server ...")
        query_cli = QUERYClient(host=self.__config.hostname,
                                port=self.__config.query_port,
                                timeout=5)
        full_stats = QueryFullStats(**dict(query_cli.get_full_stats()))
        print(f">>> {asdict(full_stats)}")
        return full_stats


class MIDDLEWARE:
    memcached: MemcachedCli = None
    minecraft: MinecraftCli = None

    def __init__(self, minecraft_conf: MinecraftConfig = None, memcached_conf: MemcachedConfig = None):
        self.memcached = MemcachedCli(config=memcached_conf)
        self.minecraft = MinecraftCli(config=minecraft_conf)

    def update_memcached_data(self):
        stats = self.minecraft.get_full_stats()
        self.memcached.insert_dict(stats)
        print(f'last insert: {self.memcached.get_from_memcached("last_insert")}')


if __name__ == '__main__':
    mine_conf = MinecraftConfig(hostname="192.168.1.3", port=5555, query_port=5556)
    mem_conf = MemcachedConfig(hostname="192.168.1.3", username='my_user', password='my_password')
    middleware = MIDDLEWARE(minecraft_conf=mine_conf, memcached_conf=mem_conf)
    # middleware.memcached.insert_dict({1: 2})
    middleware.update_memcached_data()
    # middleware.insert_dict(QueryFullStats())
    # print(mem_conf.__hash__())
    # middleware.get_full_stats()
