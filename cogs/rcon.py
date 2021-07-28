import datetime

import discord
from discord.ext import commands
from mcrcon import MCRcon
from six import BytesIO


class RCON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def login(self, ctx, ip=None, password=None):
        if ip and password:
            self.bot.rcon_cache[ctx.author.id] = {"ip": ip, "pass": password,
                                                  "expires": datetime.datetime.now() + datetime.timedelta(
                                                      minutes=10)}
            await ctx.send("Учетные данные кэшированы!")
        else:
            await ctx.send('Использование: `,login "ip" "password"`')

    @commands.command()
    async def run(self, ctx, *, command):
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
            with MCRcon(creds["ip"], creds["pass"]) as mcr:
                response = mcr.command(command)
                if len(response) <= 1800:
                    await ctx.send("Ответ: ```{}```".format(response))
                else:
                    await ctx.send("Ответ был слишком долгим.",
                                   file=discord.File(BytesIO(response.encode()), "response.txt"))
        except Exception as e:
            await ctx.send(f"`{e}`")


def setup(bot):
    bot.add_cog(RCON(bot))
