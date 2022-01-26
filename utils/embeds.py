import datetime

import discord
from discord import Embed


def status_embed(motd: str, ip: str, version: str, online_players_count: int, max_players_count: int, player_nicknames: str, tag: str) -> Embed:
    embed = discord.Embed(title="Статус сервера Rumblur", color=discord.Colour.green(),
                          timestamp=datetime.datetime.utcnow())
    embed.set_author(name="Rumblur Classic", url="https://rumblur.hrebeni.uk",
                     icon_url="https://rumblur.hrebeni.uk/images/chainfire.png")
    embed.set_thumbnail(url="https://rumblur.hrebeni.uk/images/chainfire.gif")
    embed.add_field(name="Сообщение дня", value=f"```{motd}```", inline=False)
    embed.add_field(name="IP-адрес", value=f"{ip}", inline=True)
    embed.add_field(name="Версия сервера", value=f"{version}", inline=True)
    embed.add_field(name="Статус", value="Онлайн", inline=True)
    embed.add_field(
        name=f"{online_players_count} из " + f"{max_players_count} игроков сейчас на сервере:",
        value=f"```{player_nicknames}```", inline=False)
    embed.set_footer(text=f"Rusty v{tag}", icon_url="https://rumblur.hrebeni.uk/images/paws.png")
    return embed


def admin_crash_embed(message: str) -> Embed:
    embed = discord.Embed(title="Сервер недоступен в данный момент.", description=f"Причина: `{message}`",
                          color=discord.Colour.red())
    embed.set_author(name="Having troubles...", icon_url="https://rumblur.hrebeni.uk/images/block.png")
    embed.set_thumbnail(url="https://rumblur.by/images/sadcat.png")
    embed.set_footer(text="Alerted by Rusty", icon_url="https://rumblur.hrebeni.uk/images/paws.png")
    return embed


def info_crash_embed(message: str, tag: str) -> Embed:
    embed = discord.Embed(title="Сервер недоступен", color=discord.Colour.red(),
                          timestamp=datetime.datetime.utcnow())
    embed.set_author(name="Rumblur Classic", url="https://rumblur.hrebeni.uk",
                     icon_url="https://rumblur.hrebeni.uk/images/chainfire.png")
    embed.set_thumbnail(url="https://rumblur.hrebeni.uk/images/sadcat.png")
    embed.add_field(name="Причина",
                    value=f"`{message}`", inline=False)
    embed.add_field(name="Как решить проблему?",
                    value=f"Пожалуйста, обратитесь к администрации через сообщения группы ВКонтакте или напишите в канал <#741255156242317372> с упоминанием одного из администраторов.", inline=False)
    embed.set_footer(text=f"Rusty v{tag}", icon_url="https://rumblur.hrebeni.uk/images/paws.png")
    return embed
