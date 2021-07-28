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
    async def rcon(self, ctx, ip=None):
        if ip:
            self.bot.rcon_cache[ctx.author.id] = {"ip": ip, "expires": datetime.datetime.now() + datetime.timedelta(
                minutes=10)}
            await ctx.send("Учетные данные кэшированы!")
        else:
            await ctx.send('Использование: `,login "ip"`')

    @commands.command()
    async def exec(self, ctx, *, command):
        try:
            creds = self.bot.rcon_cache[ctx.author.id]
        except:
            await ctx.send("Сначала вам нужно войти в систему с помощью `,login`")
            return
        if creds["expires"] <= datetime.datetime.now():
            self.bot.rcon_cache.pop(ctx.author.id, None)
            await ctx.send("Срок действия ваших учетных данных истек. Пожалуйста, войдите в систему еще раз.")
            return

        self.bot.rcon_cache[ctx.author.id]["expires"] = datetime.datetime.now() + datetime.timedelta(minutes=10)

        try:
            with MCRcon(creds["ip"], secret.rcon_password, secret.rcon_port) as mcr:
                response = mcr.command(command)
                pretty_response = re.sub('(§[0-9a-fA-Fkmorln])|(§\[#[0-9a-fA-F]{1,6}])|(§$)', '', response)  # BadCoder
                if len(response) <= 1800:
                    await ctx.send("Ответ: ```{}```".format(pretty_response))
                else:
                    await ctx.send("Ответ был слишком долгим.",
                                   file=discord.File(BytesIO(response.encode()), "response.txt"))
        except Exception as e:
            await ctx.send(f"`{e}`")


def setup(bot):
    bot.add_cog(RCON(bot))
