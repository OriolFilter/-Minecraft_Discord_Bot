from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from os import getenv


@dataclass
class QueryFullStats:
    """
    Used to store the values obtained from a full_query to the minecraft Server

    yikes.
    """
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

    def __post_init__(self) -> None:
        """
        Removes the character "\x1b[0m" from the fields that contains it.
        """
        if not self.players:
            self.players = []

        self.motd = self.motd.replace("\x1b[0m", '')

        new_player_list = []
        for player in self.players:
            new_player_list.append(player.replace("\x1b[0m", ''))
        self.players = new_player_list

    def __hash__(self) -> dict:
        return asdict(self)

    def __iter__(self):
        for attr, value in self.__hash__().items():
            yield attr, value


@dataclass
class _CONFIG:
    """
    Skell for other Services Configurations
    """

    def __hash__(self) -> dict:
        return asdict(self)

    def load_envs(self) -> object:
        """
        Loads variables from environment.
        :return:
        """
        raise NotImplementedError

    def __post_init__(self):
        self = self.load_envs()


@dataclass
class MinecraftConf(_CONFIG):
    """
    Stores the configuration required for the service Minecraft (using the library "mctools")

    hostname: str = "127.0.0.1"
    query_port: int = 25565
    rcon_port: int = 25575
    """
    hostname: str = "127.0.0.1"
    query_port: int = 25565
    rcon_port: int = 25575

    def load_envs(self):
        self.hostname = getenv("MINECRAFT_HOSTNAME") or self.hostname
        self.query_port = getenv("MINECRAFT_QUERY_PORT") or self.query_port
        self.rcon_port = getenv("MINECRAFT_RCON_PORT") or self.rcon_port
        return self


#  https://kb.iweb.com/hc/es/articles/230268328-C%C3%B3mo-proteger-su-servidor-del-servicio-de-Memcached

@dataclass
class MemcachedConf(_CONFIG):
    """
    Stores the configuration required for the service Memcached

    hostname: str = "127.0.0.1"
    port: int = 11211
    username: str
    password: str
    """
    hostname: str = "127.0.0.1"
    port: int = 11211
    username: str = None
    password: str = None

    def load_envs(self):
        self.hostname = getenv("MEMCACHED_HOSTNAME") or self.hostname
        self.port = getenv("MEMCACHED_PORT") or self.port
        self.username = getenv("MEMCACHED_USERNAME") or self.username
        self.password = getenv("MEMCACHED_PASSWORD") or self.password
        return self


@dataclass
class DiscordConf(_CONFIG):
    """
    Stores the configuration for the Discord Bot

    token: str
    mc_url: str : Url to post on the discord embeds / messages
    prefix: str : Prefix for the commands
    description: str : Bot description to have
    """
    token: str = None
    mc_url: str = None
    prefix: str = "!"
    description: str = "Hi, I'm a Bot!\n" \
                       "My function is to help you!"

    def load_envs(self):
        self.token = getenv("DISCORD_TOKEN") or self.token
        self.mc_url = getenv("DISCORD_MC_URL") or self.mc_url
        self.prefix = getenv("DISCORD_PREFIX") or self.prefix
        self.description = getenv("DISCORD_DESCRIPTION") or self.description
        return self


class Configuration:
    """
    Object used to store/load configurations
    """
    memcached: MemcachedConf
    minecraft: MinecraftConf
    discord: DiscordConf

    def __init__(self):
        self.memcached = MemcachedConf()
        self.minecraft = MinecraftConf()
        self.discord = DiscordConf()
