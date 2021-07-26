import os

from discord.ext import commands

minecraft_dir = '/home/artilapx/classic/'


def status():
    output = os.popen('screen -ls').read()
    if '.server' in output:
        return True
    else:
        return False


class Server(commands.Cog, command_attrs=dict(hidden=True), name="Server"):
    """Команды для взаимодействия с сервером Minecraft. Мы не можем их показать в целях безопасности."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """Запускает сервер Minecraft."""
        await ctx.send(f"Запуск сервера...")
        if not status():
            os.chdir(minecraft_dir)
            os.system('bash start.sh')
            await ctx.send(f"Сервер запущен.")
        else:
            await ctx.send(f"Сервер уже запущен и работает.")


def setup(bot):
    bot.add_cog(Server(bot))
