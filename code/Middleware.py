from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
from mctools import QUERYClient
from Classes import *
from collections.abc import Iterable
import bmemcached


class MemcachedCli:
    __config: MemcachedConf

    def __init__(self, config=None):
        if config:
            self.__config = config

    def set_config(self, config: MemcachedConf):
        self.__config = config

    # def on_set(method):
    #     """
    #     Decorator
    #     :return:
    #     """
    #
    #     @wraps(method)
    #     def wrapper(self, *args, **kwargs):
    #         try:
    #             method(self, args, kwargs)
    #             ok = True
    #         except ConnectionError:
    #             print("Connection with memcached error!!")
    #             raise ConnectionError
    #         pass
    #
    #     return wrapper

    def set(self, data: dict | QueryFullStats,*args,**kwargs) -> None:
        """
        If given QueryFullStats it transforms into a dictionary
        Iterates through the object given and inserts the data

        :param data: dictionary or QueryFullStats, Data to insert
        :return: None
        """
        print(f'[MEMCACHED] >> Inserting data')
        if isinstance(data, QueryFullStats):
            data = dict(data.__hash__())
        bmemcache_cli = bmemcached.Client(
            [f'{self.__config.hostname}:{self.__config.port}'],
            username=self.__config.username,
            password=self.__config.password)

        for key, value in data.items():
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
    __config: MinecraftConf

    def __init__(self, config=None):
        if config:
            self.__config = config

    def set_config(self, config: MinecraftConf):
        self.__config = config

    def get_full_stats(self) -> QueryFullStats:
        print("Quering from MC server ...")
        with QUERYClient(host=self.__config.hostname, port=self.__config.query_port, timeout=5) as query_cli:
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

    def __init__(self, minecraft_conf: MinecraftConf = None, memcached_conf: MemcachedConf = None,
                 cooldown: int = 10):
        self.memcached = MemcachedCli(config=memcached_conf)
        self.minecraft = MinecraftCli(config=minecraft_conf)
        if cooldown:
            self.cooldown = cooldown

    # https://stackoverflow.com/questions/1263451/python-decorators-in-classes

    def _update_minecraft_data(self) -> bool:
        """
        Queries data from the MC server and inserts it into the Memcached server
        :return: bool: If worked
        """
        print(">>> [Middleware] Updating MC data ...")
        stats = self.minecraft.get_full_stats()
        print(f">>>> [Middleware] MC stats {stats}")
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
            print("def wrapper")
            last_insert: datetime = self.memcached.get("last_insert")

            print(f"> [Middleware]  Last insert '{last_insert}'")
            if not last_insert or last_insert < (datetime.now() - timedelta(seconds=self.cooldown)):
                print(f'{last_insert} {datetime.now()}')
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
        return self.__get(key)

    @on_get
    def get_full_stats(self) -> QueryFullStats:
        result = {}
        for key, value in QueryFullStats():
            result[key] = self.memcached.get(key=key)
        return QueryFullStats(**result)


if __name__ == '__main__':
    mine_conf = MinecraftConf()
    mem_conf = MemcachedConf()
    middleware = Middleware()
    data = middleware.get_full_stats()
