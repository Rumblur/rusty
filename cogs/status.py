import asyncio
import datetime

import discord
from discord.ext import commands
from mcstatus import MinecraftServer


class Status(commands.Cog):
    """Команды, связанные со статусом сервера Rumblur."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        while True:
            await self.update_message(ctx)
            await asyncio.sleep(60)

    async def update_message(self, ctx):
        """Показывает статистику сервера Rumblur."""
        channel = ctx.bot.get_channel(741255934721916989)
        msg = await channel.fetch_message(808644874366746704)
        try:
            ip = "rumblur.by"
            server = MinecraftServer.lookup(ip)
            status = server.status()
            version = status.raw["version"]["name"]
            max_players_count = status.raw["players"]["max"]
            online_players_count = status.raw["players"]["online"]
            player_names = server.query().players.names

            server_online_status = discord.Status.online
            if online_players_count == max_players_count:
                server_online_status = discord.Status.do_not_disturb
            if int(online_players_count) == 0:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name="в пустоту")
            elif int(online_players_count) == 1:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name=f"за {online_players_count} игроком")
            else:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name=f"за {online_players_count} игроками")

            await ctx.bot.change_presence(activity=activity, status=server_online_status)

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
            emb = discord.Embed(title="Статистика сервера Rumblur", color=discord.Colour.green(),
                                timestamp=datetime.datetime.utcnow())
            emb.set_author(name="Rumblur Classic", url="https://rumblur.by",
                           icon_url="https://rumblur.by/images/chainfire.png")
            emb.set_thumbnail(url="https://rumblur.by/images/rusty.png")
            emb.add_field(name="Сообщение дня", value=f"```{motd}```", inline=False)
            emb.add_field(name="IP-адрес", value=f"{ip}", inline=True)
            emb.add_field(name="Версия сервера", value=f"{version}", inline=True)
            emb.add_field(name="Пинг", value=f"{server.ping()} мс", inline=True)
            emb.add_field(
                name=f"{online_players_count} из " + f"{max_players_count} игроков сейчас на сервере:",
                value=f"```{player_nicknames}```", inline=False)
            emb.set_footer(text="Information provided by Rusty", icon_url="https://rumblur.by/images/paws.png")
            await msg.edit(content="Слежу за сервером...")
            await msg.edit(embed=emb)
        except IOError as ex:
            emb = discord.Embed(title="Сервер недоступен", color=discord.Colour.red(),
                                timestamp=datetime.datetime.utcnow())
            emb.set_author(name="Rumblur Classic", url="https://rumblur.by",
                           icon_url="https://rumblur.by/images/chainfire.png")
            emb.set_thumbnail(url="https://rumblur.by/images/sadcat.png")
            emb.add_field(name="Причина",
                          value=f"`{ex}`", inline=False)
            emb.add_field(name="Как решить проблему?",
                          value=f"Пожалуйста, обратитесь к администрации через сообщения группы ВК.", inline=False)
            emb.set_footer(text="Information provided by Rusty", icon_url="https://rumblur.by/images/paws.png")
            await msg.edit(content="Слежу за сервером...")
            await msg.edit(embed=emb)
        except:
            await ctx.send("Что-то пошло не так.")


def setup(bot):
    bot.add_cog(Status(bot))
