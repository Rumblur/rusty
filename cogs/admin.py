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


def setup(bot):
    bot.add_cog(Admin(bot))
