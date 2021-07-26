import time

from discord.ext import commands


class Misc(commands.Cog):
    """Дополнительные команды."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Проверка пинга."""
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send(f"🏓 Pong!: {round((t2 - t1) * 1000)}мс")


def setup(bot):
    bot.add_cog(Misc(bot))
