from discord.ext import commands
from Classes import Config, MinecraftConfig, MemcachedConfig
from Middleware import Middleware

if __name__ == '__main__':
    mine_conf = MinecraftConfig(hostname="192.168.1.3", port=5555, query_port=5556)
    mem_conf = MemcachedConfig(hostname="192.168.1.3", username='my_user', password='my_password')
    middleware = Middleware(minecraft_conf=mine_conf, memcached_conf=mem_conf)

description = '''Welcome welcome, im a fucking bot'''
client = commands.Bot(command_prefix="m.", description=description)
# client.remove_command('help')

print('Starting minecraft discord bot...')


@client.event
async def on_ready():
    print('------')
    print('Logged as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # await client.change_presence(status=client.Status.idle, activity=game)
    # game = client.Game("Hey, fuck off")
    # await client.change_presence(status=client.change_presence().Status.online, activity=game)
    # logging.info('Bot is running...')


# # Checks
# def ran_in_server():
#     def predicate(ctx):
#         return int(ctx.guild.id)==int(json.server_id)
#     return commands.check(predicate)
#
# async def add_log(message:str):
#     if json.log_channel_id: await bot.get_channel(int(json.log_channel_id)).send(message)
#
# def has_role(user, role):
#     if role in user.roles:return True
#
# def get_role(ctx,role_name):
#     role_id = json.role_list[role_name]
#     role = discord.utils.get(ctx.guild.roles, id=int(role_id))
#     return role
#
#
# async def toggle_role(ctx,user, role):
#     try:
#         if has_role(user, role):
#             await user.remove_roles(role)
#             await add_log(f'{user.mention} removed the role {role.mention}')
#         else:
#             await user.add_roles(role)
#             await add_log(f'{user.mention} received the role {role.mention}')
#     except discord.Forbidden:
#         ctx.send('The bot lacks permission to administrate roles...')
#
#
# @bot.command()
# @ran_in_server()
# async def news(ctx) : #pass user and role
#     role=get_role(ctx,'news')
#     await toggle_role(ctx,ctx.author,role)
#
# @client.command()
# async def ip(ctx):
#     await ctx.send('Server IP:'
#                    f'``` {api.ip}```')
#
# @ran_in_server()

def __get_status_message(data: Middleware.get_full_stats):
    txt = '\n' \
          '`{server_name}`\n' \
          '```yml\n' \
          'Status: {status}\n' \
          'Players: {num_players}/{max_players}\n' \
          'Current_players:\n' \
          '{player_list}\n' \
          '```'.format(status="Online",
                       server_name=data.motd,
                       num_players=data.numplayers,
                       max_players=data.maxplayers,
                       player_list="".join([f'  -  {playername}\n' for playername in data.players]))
    return txt


@client.command()
async def status(ctx):  # pass user and role
    data = middleware.get_full_stats()
    online = True
    if online: await ctx.send(__get_status_message(data))
    # fer servir un dictionary...
    # else: ctx.send(__get__offline__status_message(data))

    # f'Player list:\n'\
    # f'{}'\
    # '```'

    # await ctx.send(f'```\n'
    #                    f'Minecraft server is currently Running\n'
    #                    f'Players online {api.minecraft_players_online}/{api.minecraft_players_max}\n'
    #                    f'Player list:\n'
    #                    f'{}'
    #                    '```')
    # status=api.sastatus_code
    # if not status:
    #     await ctx.send(f'```\n'
    #                    f'Minecraft server is currently Down\n'
    #                    '```')
    # else:


#    role=get_role(ctx,'news')x
#    await toggle_role(ctx,ctx.author,role)

# ## extra
#
@client.command()
async def invite(ctx):
    url = "https://discord.com/oauth2/authorize?client_id=975398947461943387&permissions=377957223488&scope=bot"
    await ctx.send(url)


token = ''
client.run()
