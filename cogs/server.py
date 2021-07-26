import os

from discord.ext import commands


class Server(commands.Cog, command_attrs=dict(hidden=True), name="Server"):
    """Команды для взаимодействия с сервером Minecraft. Мы не можем их показать в целях безопасности."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """Запускает сервер Minecraft."""
        # TODO Проверить запуск dummy скрипта
        os.system('./classic/bash start.sh')
        await ctx.send(f"Запуск сервера...")


def setup(bot):
    bot.add_cog(Server(bot))
