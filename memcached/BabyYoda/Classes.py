from dataclasses import dataclass, asdict
from mctools import QUERYClient
import bmemcached
from datetime import datetime, timedelta
from functools import wraps


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
    last_insert: datetime = None
    connected: bool = False

    def __post_init__(self):
        if not self.players: self.players = []

        self.motd = self.motd.replace("\x1b[0m", '')

        new_player_list = []
        for player in self.players:
            new_player_list.append(player.replace("\x1b[0m", ''))
        self.players = new_player_list

    def __hash__(self) -> dict:
        return asdict(self)


class MemcachedCli:
    __config: MemcachedConfig

    def __init__(self, config=None):
        if config:
            self.__config = config

    def set_config(self, config: MemcachedConfig):

        self.__config = config

    def insert(self, data: dict | QueryFullStats) -> None:
        """
        Inserts given data into the MemcachedServer
        Intended for dictionary usage, if QueryFullStats object is passed it gets transformed into a dictionary

        :param data: dictionary or QueryFullStats, Data to insert
        :return: None
        """
        if isinstance(data, QueryFullStats): data = dict(data.__hash__())
        memcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)

        for key, value in data.items():
            # assert key, value
            print(f"[MEMCACHED] >>> Inserting {key}({value})")
            memcache_cli.set(key, value)

    def get(self, key: str) -> int | str | dict | datetime:
        memcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)
        return memcache_cli.get(key=key)


class MinecraftCli:
    __config: MinecraftConfig

    def __init__(self, config=None):
        if config:
            self.__config = config

    def set_config(self, config: MinecraftConfig):
        self.__config = config

    def get_full_stats(self) -> QueryFullStats:
        print("Quering from MC server ...")
        query_cli = QUERYClient(host=self.__config.hostname,
                                port=self.__config.query_port,
                                timeout=5)
        _full_stats_query: dict = query_cli.get_full_stats()
        _full_stats_query["last_insert"] = datetime.now()
        _full_stats_query["connected"] = False
        full_stats_object = QueryFullStats(**dict(_full_stats_query))
        print(f">>> {asdict(full_stats_object)}")
        return full_stats_object


class MIDDLEWARE:
    memcached: MemcachedCli = None
    minecraft: MinecraftCli = None

    def __init__(self, minecraft_conf: MinecraftConfig = None, memcached_conf: MemcachedConfig = None):
        self.memcached = MemcachedCli(config=memcached_conf)
        self.minecraft = MinecraftCli(config=minecraft_conf)

        # self.get=self._decorator_get_data(self.get)
#https://stackoverflow.com/questions/1263451/python-decorators-in-classes
    def _update_minecraft_data(self) -> bool:
        """
        Queries data from the MC server and inserts it into the Memcached server
        :return: bool: If worked
        """
        print(">>> [Middleware] Updating MC data ...")
        stats = self.minecraft.get_full_stats()
        self.memcached.insert(stats)
        return True
        # print(f'last insert: {self.memcached.get("last_insert")}')


    def _decorator(func):
        def magic(*args, **kwargs):
            print("start magic")
            result = func(*args, **kwargs)
            print("end magic")
            return result
        return magic

    def _decorator_get_data(method):
        """
        Checks if still on cooldown before running the given command
        :param func:
        :return:
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            cooldown = 10
            last_insert: datetime = self.memcached.get("last_insert")
            # result: bool = False
            print(f"> [Middleware]  Last insert '{last_insert}'")
            if not last_insert or last_insert < (datetime.now() - timedelta(seconds=cooldown)):
                print(">> [Middleware] Requesting data update")
                self._update_minecraft_data()
            else:
                print(">> [Middleware] Still on cooldown, skipping ...")

            # if result:if
            result = method(self,*args, **kwargs)
            # else:
            #     print(">> [Middlware] Error updating ...")

            return result

        # @classmethod


        return wrapper

    @_decorator_get_data
    def get(self, key):
        # Should allow using a list/touple
        return self.memcached.get(key=key)


if __name__ == '__main__':
    mine_conf = MinecraftConfig(hostname="192.168.1.3", port=5555, query_port=5556)
    mem_conf = MemcachedConfig(hostname="192.168.1.3", username='my_user', password='my_password')
    middleware = MIDDLEWARE(minecraft_conf=mine_conf, memcached_conf=mem_conf)
    print(middleware.get(key="players"))

