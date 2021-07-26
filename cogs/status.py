import datetime

import discord
from discord.ext import commands
from mcstatus import MinecraftServer


class Status(commands.Cog):
    """Команды, связанные со статусом сервера Rumblur."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx):
        """Показывает статистику сервера Rumblur."""
        await ctx.trigger_typing()
        try:
            ip = "rumblur.by"
            server = MinecraftServer.lookup(ip)
            status = server.status()
            version = status.raw["version"]["name"]
            max_players_count = status.raw["players"]["max"]
            online_players_count = status.raw["players"]["online"]
            player_names = server.query().players.names

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
            await ctx.send(embed=emb)
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
            await ctx.send(embed=emb)
        except:
            await ctx.send("Что-то пошло не так.")


def setup(bot):
    bot.add_cog(Status(bot))
