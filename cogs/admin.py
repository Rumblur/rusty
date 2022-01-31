import os
from datetime import datetime

from discord.ext import commands
from git import Repo

from modules import utils
from modules.embeds import admin_notice


class Admin(commands.Cog, name="Admin"):
    """Команды для администраторов."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", brief="Shutdown the bot", description="It just restarts")
    async def shutdown(self, ctx):
        """Выключает бота."""
        if utils.is_admin(ctx.message.author.id):
            await ctx.send("Пока!")
            await self.bot.close()
        else:
            await ctx.send(embed=await admin_notice())

    @commands.command(name="pull", brief="Update the bot", description="It just does git pull")
    async def git_update(self, ctx):
        """Обновляет бота с GitHub."""
        if utils.is_admin(ctx.message.author.id):
            now = datetime.now()
            message = ""
            repo = Repo(path=os.getcwd())
            o = repo.remotes.origin
            for fetch_info in o.pull():
                message += f"\n Updated '{fetch_info.ref}' to '{fetch_info.commit}'"
            later = datetime.now()
            difference = (later - now).total_seconds()
            await ctx.send(f"Операция выполнена успешно за {difference} с. Вывод: ```prolog\n{message}\n```")
        else:
            await ctx.send(embed=await admin_notice())


def setup(bot):
    bot.add_cog(Admin(bot))
