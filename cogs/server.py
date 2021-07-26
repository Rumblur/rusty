import os

from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        # TODO Проверить запуск dummy скрипта
        os.system('./classic/bash start.sh')
        await ctx.send(f"Запуск сервера...")


def setup(bot):
    bot.add_cog(Server(bot))
