import bmemcached
from discord.ext import commands
from discord import Embed
from Classes import Configuration, DiscordConf
from Middleware import Middleware


class Bot(commands.Bot):
    conf: DiscordConf = None
    Middleware: Middleware = None

    def __init__(self, conf: Configuration = None, *args, **kwargs):
        super(commands.Bot, self).__init__(command_prefix=conf.discord.prefix, description=conf.discord.description,
                                           self_bot=False)
        self.config = conf.discord
        self.Middleware = Middleware(minecraft_conf=conf.minecraft, memcached_conf=conf.memcached)
        self.add_commands()

    def run(self, *args, **kwargs):
        super(commands.Bot, self).run(self.config.token, *args, **kwargs)

    async def on_ready(self):
        print('------')
        print('Logged as')
        print(self.user.name)
        print(self.user.id)
        print(f'invite me with: https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot')
        print('------')

    def __generate_embed(self, *args, **kwargs) -> Embed:
        embed = Embed(colour=kwargs.pop("colour"))
        embed.set_author(name=self.user.name,
                         icon_url=self.user.avatar_url)
        embed.set_footer(text=self.config.mc_url)
        return embed

    def Embed(self, ok: bool = True) -> Embed:
        return self.__generate_embed(colour=(0xff9494, 0x88ff70)[ok])

    def embed_version(self, embed: Embed):
        embed.add_field(name="Server Version:",
                        value=self.Middleware.get("version"),
                        inline=True)

    def embed_active_players(self, embed: Embed):
        """
        Adds a field to the embed.

        n_x/n_max_players
        :param embed:
        :return: given_object
        """
        embed.add_field(name="Active players:",
                        value=f'{self.Middleware.get("numplayers")}/{self.Middleware.get("maxplayers")}',
                        inline=True)

    def embed_player_list(self, embed: Embed):
        """
        Adds a field to the embed.

        n_x/n_max_players
        :param embed:
        :return: given_object
        """
        embed.add_field(name="Player List:",
                        value="".join([f'  -  {playername}\n' for playername in self.Middleware.get('players')]),
                        inline=False)

    def add_commands(self):
        @self.command()
        async def status(ctx):
            """
            Returns an embed that stores status regarding the minecraft server

            :param ctx:
            :return:
            """
            try:
                embed = self.Embed()
                embed.add_field(name=self.Middleware.get('motd'), value="-", inline=False)
                self.embed_active_players(embed)
                self.embed_version(embed)
                self.embed_player_list(embed)
                await ctx.send(embed=embed)
            except TimeoutError as e:
                print(f"[Error] {e}")
                embed = self.Embed(ok=False)
                embed.add_field(name="Error connecting to the server",
                                value="This could be due inactivity on the minecraft "
                                      "server, please ensure the connection and try "
                                      "again later.", inline=False)
                await ctx.send(embed=embed)

            except bmemcached.exceptions.MemcachedException as e:
                print(f"[Error] {e}")
                embed = self.Embed(ok=False)
                embed.add_field(name="Error connecting/authenticating to the cache server",
                                value="Please contact an administrator", inline=False)
                await ctx.send(embed=embed)

            except Exception as e:
                print(f"[Unexpected Error] {e}")
                embed = self.Embed(ok=False)
                embed.add_field(name="Unexpected error",
                                value="Please contact an administrator", inline=False)
                await ctx.send(embed=embed)