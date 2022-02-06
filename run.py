import asyncio
import json
import os
import re
import signal
import socket
import subprocess
import sys
from socket import timeout, gaierror

import discord
from discord.ext import commands, tasks
from mcstatus import MinecraftServer

import secret
from modules import mcrcon
from modules.embeds import status_embed, info_crash_embed, admin_crash_embed
from modules.status import build_player_list, build_motd

client = commands.Bot(command_prefix=",")
client.remove_command('help')

server_responding = False
skip_check = True
use_query = True

ADMIN_CHANNEL_ID = 0
INFO_MESSAGE = 0

if os.path.exists('config.json'):
    with open('config.json') as file:
        config = json.load(file)
else:
    print("No configuration file detected.")
    sys.exit()

server = MinecraftServer.lookup(f"{config['servers'][0]['ip']}:{config['servers'][0]['port']}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.path.exists('data'):
    print("Please configure this bot according to readme file.")
    sys.exit("data folder and it's contents are missing")


def get_git_tag() -> str:
    return subprocess.check_output(['git', 'describe', '--tags']).decode('ascii').strip()


def list_module(directory):
    return (f for f in os.listdir(directory) if f.endswith('.py'))


def connect():
    sock.connect((config['servers'][0]['ip'], secret.rcon_port))
    mcrcon.login(sock, secret.rcon_password)


connect()

last_message = None


@client.event
async def on_ready():
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\ndiscord.py version: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!\n')

    # Load Modules
    module_folders = ['cogs']
    for module in module_folders:
        for extension in list_module(module):
            try:
                client.load_extension(f'{module}.{os.path.splitext(extension)[0]}')
                print(f"Loaded {extension} cog")
            except Exception as ex:
                print(f"Failed to load module {module}.{os.path.splitext(extension)[0]}.", file=sys.stderr)
                print(ex)

    bridge_loop.start()
    print("Bridge from Minecraft to Discord and vice versa activated.")
    client.loop.create_task(check_server_status())
    print("Checking server status.")
    try:
        client.loop.add_signal_handler(signal.SIGINT, shutdown)
        client.loop.add_signal_handler(signal.SIGTERM, shutdown)
    except NotImplementedError:
        pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id in config["bridgeChannels"]:
        to_chat(message)


# BRIDGE --->

def to_chat(message):
    messageText = message.clean_content
    customEmoji = re.compile("<:.*:\d*>")
    emojiName = re.compile(":(?<=:)(.*)(?=:):")
    for emoji in customEmoji.findall(messageText):
        messageText = messageText.replace(emoji, emojiName.search(emoji).group())
    for attachment in message.attachements:
        messageText += f" {attachment.url}"
    command = """tellraw @a ["",{"text":"["},{"text":"%s","color":"dark_aqua"},{"text":" | "},{"text":"#%s","color":"dark_aqua"},{"text":"] %s"}]""" % (
        message.author.display_name, message.channel.name, messageText)
    try:
        mcrcon.command(sock, command)
    except:
        connect()


def parse_log_line(line):
    ret = re.findall("(?<=\[)(.+?)(?=\])", line)[:2]
    ret.append(re.search("(?<=: )(.*)(?=\n)", line).group())
    return ret


def parse_chat_message(message_type, content):
    if message_type != "Server thread/INFO":
        return False
    nick_match = re.search("(?<=<)(.*)(?=>)", content)
    if nick_match is None:
        return False
    nick = nick_match.group()
    message = content[nick_match.end() + 2:]
    mentions = re.findall("@.*?#\d{4}", message)
    for mention in mentions:
        for member in client.get_all_members():
            if f"@{member.name}#{member.discriminator}" == mention:
                message = message.replace(mention, member.mention)
    return nick, message


def parse_events(message_type, content):
    if message_type != "Server thread/INFO":
        return False
    words = content.split(' ')
    if re.search(".+? вернулся из небытия!", content) is not None:
        return 1, [words[0]]
    elif re.search(".+? ушёл в небытие!", content) is not None:
        return 2, [words[0]]
    elif words[0] == "*":
        return 3, [words[1], " ".join(words[2:])]


async def send_to_discord(message):
    for channel_id in config["bridgeChannels"]:
        await client.get_channel(channel_id).send(message)


@tasks.loop()
async def bridge_loop():
    global last_message
    with open(config['servers'][0]['log']) as log_file:
        last_line = list(log_file)[-1]
        if last_message != last_line:
            last_message = last_line
            time, message_type, content = parse_log_line(last_line)
            chat_message = parse_chat_message(message_type, content)
            if chat_message:
                nick, message = chat_message
                await send_to_discord(f"<{nick}> {message}")
            else:
                events = parse_events(message_type, content)
                if events:
                    event, parameters = events
                    if event == 1:
                        await send_to_discord(f":heavy_plus_sign: **{parameters[0]}** joined.")
                    elif event == 2:
                        await send_to_discord(f":heavy_minus_sign: **{parameters[0]}** left.")
                    elif event == 3:
                        await send_to_discord(f":thought_balloon: **{parameters[0]}** {parameters[1]}")


# BRIDGE <---

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

            await update_presence(num_players, max_players)
            await INFO_MESSAGE.edit(content="Слежу за сервером...",
                                    embed=status_embed(build_motd(server.status()),
                                                       f"{config['servers'][0]['ip']}",
                                                       version,
                                                       num_players,
                                                       max_players,
                                                       build_player_list(num_players, player_names)))
            await asyncio.sleep(60)
        else:
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching,
                                          name=f"на мёртвый сервер"),
                status=discord.Status.dnd)
            await INFO_MESSAGE.edit(content="Whoops...",
                                    embed=info_crash_embed("Connection to server refused", get_git_tag()))
            await ADMIN_CHANNEL_ID.send(embed=admin_crash_embed("Connection to server refused"))
            await asyncio.sleep(180)


def shutdown():
    print("Shutting down, please wait...", file=sys.stderr)
    client.loop.stop()


@client.event
async def on_disconnect():
    print("Disconnected. Reconnecting...")
    await client.wait_until_ready()
    print("Reconnected.")


client.run(secret.token, reconnect=True)
sock.close()
