from discord.ext import commands


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


def setup(bot):
    bot.add_cog(Admin(bot))
