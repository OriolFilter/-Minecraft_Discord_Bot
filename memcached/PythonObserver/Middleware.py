from dataclasses import dataclass
from mctools import QUERYClient


@dataclass()
class _CONFIG:
    hostname: str = None
    port: int = None

@dataclass()
class ConfigMinecraftServer(_CONFIG):
    query_port: int = 25565
    rcon_port: int = 25575
    port: int = 25565


class ConfigMemcachedServer(_CONFIG):
    pass


class MIDDLEWARE:
    __memcached_server_conf: ConfigMemcachedServer = None
    __minecraft_server_conf: ConfigMinecraftServer = None

    def __init__(self):
        self.__minecraft_server_conf = ConfigMinecraftServer(hostname="192.168.1.3", port=5555, query_port=5556)
        print(self.__minecraft_server_conf)
        pass

    # def query(self): init_query_client
    # def query_end(self): close_query_client
    # @query

    def get_minecraft_players(self):
        query = QUERYClient(host=self.__minecraft_server_conf.hostname, port=self.__minecraft_server_conf.query_port, timeout=5)
        print(query.get_basic_stats())
        print(query.get_full_stats())
        pass


if __name__ == '__main__':
    pass
    middleware = MIDDLEWARE()

    middleware.get_minecraft_players()
