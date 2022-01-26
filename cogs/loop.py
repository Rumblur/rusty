import asyncio
import subprocess

import discord
from discord.ext import commands, tasks
from mcstatus import MinecraftServer

from utils.embeds import admin_crash_embed, info_crash_embed, status_embed


def get_git_tag() -> str:
    return subprocess.check_output(['git', 'describe', '--tags']).decode('ascii').strip()


class Loop(commands.Cog):
    """Цикл."""

    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.check_server_status.start()

    def cog_unload(self):
        self.check_server_status.cancel()

    async def do_loop(self):
        info_channel = self.bot.get_channel(741255934721916989)
        admin_channel = self.bot.get_channel(741254660026925147)
        msg = await info_channel.fetch_message(808644874366746704)
        while True:
            try:
                ip = "rumblur.hrebeni.uk"
                server = MinecraftServer.lookup(ip)
                status = server.status()
                version = status.raw["version"]["name"]
                max_players_count = status.raw["players"]["max"]
                online_players_count = status.raw["players"]["online"]
                player_names = server.query().players.names

                if int(online_players_count) == 0:
                    await self.bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching, name="в пустоту"),
                        status=discord.Status.idle)
                elif int(online_players_count) == 1:
                    await self.bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name=f"за {online_players_count} игроком"),
                        status=discord.Status.online)
                elif int(online_players_count) == max_players_count:
                    await self.bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name=f"за {online_players_count} игроками"),
                        status=discord.Status.dnd)
                else:
                    await self.bot.change_presence(
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                  name=f"за {online_players_count} игроками"),
                        status=discord.Status.online)

                if int(online_players_count) > 0:
                    num = 1
                    player_nicknames = "\n"
                    for player in player_names:
                        player_nicknames += str(num) + ". " + player + "\n"
                        num += 1
                    player_nicknames += ""
                else:
                    player_nicknames = "Никого нет на сервере..."

                if isinstance(status.raw["description"], dict):
                    num = len(status.raw["description"]["extra"])
                    x = 0
                    y = 0
                    all = []
                    while True:
                        if x != num:
                            motd_final = status.raw["description"]["extra"][x]
                            all.append(motd_final["text"])
                            x += 1
                            y += 1
                        else:
                            motd = "".join(all)
                            break
                else:
                    motd = status.raw["description"]
                await msg.edit(content="Слежу за сервером...")
                await msg.edit(
                    embed=status_embed(motd, ip, version, online_players_count, max_players_count, player_nicknames,
                                       get_git_tag()))
            except IOError as ex:
                # Set presence
                await self.bot.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching,
                                              name=f"на мёртвый сервер"),
                    status=discord.Status.dnd)

                await msg.edit(content="Whoops...")
                await msg.edit(embed=info_crash_embed(ex, get_git_tag()))
                await admin_channel.send(embed=admin_crash_embed(ex))

    @tasks.loop(minutes=1.0)
    async def check_server_status(self):
        async with self.lock:
            await self.do_loop()

    @check_server_status.after_loop
    async def on_loop_cancel(self):
        admin_channel = self.bot.get_channel(741254660026925147)
        if self.check_server_status.is_being_cancelled():
            await admin_channel.send("Wtf, server status checking cancelled?")

    @check_server_status.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Loop(bot))
