from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
from mctools import QUERYClient
from Classes import *
from collections.abc import Iterable
import bmemcached


class MemcachedCli:
    __config: MemcachedConfig

    def __init__(self, config=None):
        if config:
            self.__config = config

    def set_config(self, config: MemcachedConfig):

        self.__config = config

    def on_set(method):
        """
        Decorator
        :return:
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):

            try:
                method()
                ok = True
            except ConnectionError:
                # self.memcached.set({})
                print("Connection with memcached error!!")
                raise ConnectionError
            pass

        return wrapper

    def set(self, data: dict | QueryFullStats) -> None:
        """
        If given QueryFullStats it transforms into a dictionary
        Iterates through the object given and inserts the data

        :param data: dictionary or QueryFullStats, Data to insert
        :return: None
        """
        if isinstance(data, QueryFullStats):
            data = dict(data.__hash__())
        print(data)
        bmemcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)

        for key, value in data.items():
            # assert key, value
            print(f"[MEMCACHED] >>> Inserting {key}({value})")
            bmemcache_cli.set(key, value)

    def __get(self, key: str, *args, **kwargs) -> dict | str | int | datetime:
        bmemcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)
        return bmemcache_cli.get(key)

    def get(self, key: dict | QueryFullStats) -> int | str | dict | datetime:
        return self.__get(key)


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


class Middleware:
    memcached: MemcachedCli = None
    minecraft: MinecraftCli = None
    cooldown: int

    def __init__(self, minecraft_conf: MinecraftConfig = None, memcached_conf: MemcachedConfig = None, cooldown:int = 10):
        self.memcached = MemcachedCli(config=memcached_conf)
        self.minecraft = MinecraftCli(config=minecraft_conf)
        if cooldown: self.cooldown = cooldown

        # self.get=self._decorator_get_data(self.get)

    # https://stackoverflow.com/questions/1263451/python-decorators-in-classes
    def _update_minecraft_data(self) -> bool:
        """
        Queries data from the MC server and inserts it into the Memcached server
        :return: bool: If worked
        """
        print(">>> [Middleware] Updating MC data ...")
        stats = self.minecraft.get_full_stats()
        self.memcached.set(stats)
        return True

    def on_get(method):
        """
        Checks if still on cooldown before running the given command
        :param func:
        :return:
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            last_insert: datetime = self.memcached.get("last_insert")
            # result: bool = False
            print(f"> [Middleware]  Last insert '{last_insert}'")
            if not last_insert or last_insert < (datetime.now() - timedelta(seconds=self.cooldown)):
                print(">> [Middleware] Requesting data update")
                self._update_minecraft_data()
            else:
                print(">> [Middleware] Still on cooldown, skipping ...")
            result = method(self, *args, **kwargs)
            return result

        return wrapper

    def __get(self, *args, **kwargs):
        return self.memcached.get(*args, **kwargs)

    @on_get
    def get(self, key) -> int | str | datetime:
        # Should allow using a list/touple
        return self.__get(key)

    @on_get
    def get_full_stats(self) -> QueryFullStats:
        result = {}
        for key, value in QueryFullStats():
            result[key] = self.memcached.get(key=key)
        return QueryFullStats(**result)

        # return self.__get(QueryFullStats())


if __name__ == '__main__':
    mine_conf = MinecraftConfig(hostname="192.168.1.3", port=5555, query_port=5556)
    mem_conf = MemcachedConfig(hostname="192.168.1.3", username='my_user', password='my_password')
    middleware = Middleware(minecraft_conf=mine_conf, memcached_conf=mem_conf)
    data = middleware.get_full_stats()
    # print(data)
    # print(data.motd)
    txt = '\n' \
          '`{server_name}`\n' \
          '```yaml' \
          'Status: {status}\n' \
          'Players: {num_players}/{max_players}\n' \
          'Player_list:' \
          '{player_list}\n```' \
          ''.format(status="Online",
                    server_name=data.motd,
                    num_players=data.numplayers,
                    max_players=data.maxplayers,
                    player_list="".join([f'  - {playername}\n' for playername in data.players]))
    # print("{x}".format(x=3))
          # '```'.format(server_name=2,status,2)
    # print()

    # f'{"\n".join([playername for playername in data.players])}'
    print(txt)
    # print(middleware.get(key="players"))
    # middleware.get_full_stats()
