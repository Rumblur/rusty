import os
from datetime import datetime

from discord.ext import commands
from git import Repo


class Admin(commands.Cog, command_attrs=dict(hidden=True), name="Admin"):
    """К сожалению, мы не можем показать команды в целях безопасности."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Выключает бота."""
        await ctx.send("Пока!")
        await self.bot.close()

    @commands.command(name='pull')
    @commands.has_permissions(administrator=True)
    async def git_update(self, ctx):
        """Обновляет бота с GitHub."""
        now = datetime.now()
        message = ""
        repo = Repo(path=os.getcwd())
        o = repo.remotes.origin
        for fetch_info in o.pull():
            message += f"\n Updated '{fetch_info.ref}' to '{fetch_info.commit}'"
        later = datetime.now()
        difference = (later - now).total_seconds()
        await ctx.send(f"Операция выполнена успешно за {difference} с. Вывод: ```prolog\n{message}\n```")


def setup(bot):
    bot.add_cog(Admin(bot))
