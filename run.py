import os
import sys
import traceback

import discord
from discord.ext import commands

import secret

client = commands.Bot(command_prefix=",")
client.remove_command('help')


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
            except Exception:
                print(f'Failed to load module {module}.{os.path.splitext(extension)[0]}.', file=sys.stderr)
                traceback.print_exc()


client.run(secret.secret)
