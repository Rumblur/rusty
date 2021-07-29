import datetime
import re

import discord
from discord.ext import commands
from mcrcon import MCRcon
from six import BytesIO

import secret


class RCON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def exec(self, ctx, *, command=None):
        try:
            if command:
                with MCRcon("rumblur.by", secret.rcon_password, secret.rcon_port) as mcr:
                    response = mcr.command(command)
                    # BadCoder
                    pretty_response = re.sub('(§[0-9a-fA-Fkmorln])|(§\[#[0-9a-fA-F]{1,6}])|(§$)', '', response)
                    if len(response) <= 1800:
                        await ctx.send("Ответ: ```{}```".format(pretty_response))
                    else:
                        await ctx.send("Ответ был слишком долгим.",
                                       file=discord.File(BytesIO(response.encode()), "response.txt"))
            else:
                await ctx.send('Использование: `,exec "command без /, как в консоли"`')
        except Exception as e:
            await ctx.send(f"`{e}`")


def setup(bot):
    bot.add_cog(RCON(bot))
