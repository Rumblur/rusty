import asyncio
import os
import subprocess
import sys
import time
from socket import timeout, gaierror

import discord
from discord.ext import commands
from mcstatus import MinecraftServer

import secret
from modules.embeds import status_embed, info_crash_embed, admin_crash_embed
from modules.status import build_player_list, build_motd

client = commands.Bot(command_prefix=",")
client.remove_command('help')

server_responding = False
skip_check = True
use_query = True

ADMIN_CHANNEL_ID = 0
INFO_MESSAGE = 0

IP = "rumblur.hrebeni.uk"

server = MinecraftServer.lookup(IP)

if not os.path.exists('data'):
    print("Please configure this bot according to readme file.")
    sys.exit("data folder and it's contents are missing")


def get_git_tag() -> str:
    return subprocess.check_output(['git', 'describe', '--tags']).decode('ascii').strip()


def list_module(directory):
    return (f for f in os.listdir(directory) if f.endswith('.py'))


@client.event
async def on_ready():
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\ndiscord.py version: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')

    # Load Modules
    module_folders = ['cogs']
    for module in module_folders:
        for extension in list_module(module):
            try:
                client.load_extension(f'{module}.{os.path.splitext(extension)[0]}')
            except Exception as ex:
                print(f'Failed to load module {module}.{os.path.splitext(extension)[0]}.', file=sys.stderr)
                print(ex)

    try:
        print("Checking the status of Rumblur server via the ping protocol...")
        server.status()
        print("Connected to server.")
        server.query()
        print("Using query protocol...")
        print("Checking server version...")
        print(f"Version of server: {server.query().software.version}")
        print(f"Server using {server.query().software.brand}. Starting checking status loop.")
    except timeout:
        print("Timeout, stopping using query...")
    except (ConnectionRefusedError, gaierror):
        print("Connection to server refused, set loop time to 30 seconds...")

    await check_server_status()


async def update_presence(num_players: int, max_players: int):
    if int(num_players) == 0:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="в пустоту"),
            status=discord.Status.idle)
    elif int(num_players) == 1:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"за {num_players} игроком"),
            status=discord.Status.online)
    elif int(num_players) == max_players:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"за {num_players} игроками"),
            status=discord.Status.dnd)
    else:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                      name=f"за {num_players} игроками"),
            status=discord.Status.online)


async def check_server_status():
    """
    Async function that runs forever
    It is used to check server status.
    """
    global server_responding, skip_check, use_query, ADMIN_CHANNEL_ID, INFO_MESSAGE
    INFO_CHANNEL_ID = client.get_channel(741255934721916989)
    ADMIN_CHANNEL_ID = client.get_channel(741254660026925147)
    INFO_MESSAGE = await INFO_CHANNEL_ID.fetch_message(808644874366746704)

    await client.wait_until_ready()
    while not client.is_closed():
        try:
            server.status()
            skip_check = False
            server_responding = True
            server.query()
            use_query = True
        except timeout:
            use_query = False
        except (ConnectionRefusedError, gaierror):
            skip_check = True
            server_responding = False

        if server_responding:
            if skip_check:
                num_players = 0
                max_players = 0
                player_names = ""
                version = "N/A"
                ping = "N/A"
            else:
                if use_query:
                    num_players = server.query().players.online
                    max_players = server.query().players.max
                    player_names = server.query().players.names
                    version = server.query().software.version
                else:
                    num_players = server.status().players.online
                    max_players = server.status().players.max
                    player_names = ""
                    version = server.status().version.name

                t1 = time.perf_counter()
                t2 = time.perf_counter()
                ping = f"{round((t2 - t1) * 1000)} мс"

            await update_presence(num_players, max_players)
            await INFO_MESSAGE.edit(content="Слежу за сервером...",
                                    embed=status_embed(build_motd(server.status()),
                                                       IP,
                                                       version,
                                                       ping,
                                                       num_players,
                                                       max_players,
                                                       build_player_list(num_players, player_names),
                                                       get_git_tag()))
            await asyncio.sleep(60)
        else:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching,
                                          name=f"на мёртвый сервер"),
                status=discord.Status.dnd)
            await INFO_MESSAGE.edit(content="Whoops...", embed=info_crash_embed("Connection to server refused", get_git_tag()))
            await ADMIN_CHANNEL_ID.send(embed=admin_crash_embed("Connection to server refused"))
            await asyncio.sleep(180)


@client.event
async def on_disconnect():
    print("Disconnected...")


client.run(secret.token, reconnect=True)
