import datetime
import re

import discord
from discord.ext import commands
from mcrcon import MCRcon
from six import BytesIO

import secret


class RCON(commands.Cog, command_attrs=dict(hidden=True), name="RCON"):
    """Команды, предназначенные для управления сервером через чат Discord. Мы не можем их показать в целях безопасности."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def exec(self, ctx, *, command=None):
        try:
            if command:
                with MCRcon("rumblur.hrebeni.uk", secret.rcon_password, secret.rcon_port) as mcr:
                    response = mcr.command(command)
                    # BadCoder
                    pretty_response = re.sub('(§[0-9a-fA-Fkmorln])|(§\[#[0-9a-fA-F]{1,6}])|(§$)', '', response)
                    if len(response) <= 1800:
                        await ctx.send(f"Ответ: ```{pretty_response}```")
                    elif len(response) == 0:
                        await ctx.send("`Пустой ответ`")
                    else:
                        await ctx.send("`Ответ был слишком большим.`",
                                       file=discord.File(BytesIO(response.encode()), "response.txt"))
            else:
                await ctx.send('Использование: `,exec "command без /, как в консоли"`')
        except Exception as e:
            await ctx.send(f"`{e}`")


def setup(bot):
    bot.add_cog(RCON(bot))
