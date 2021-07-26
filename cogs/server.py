import os

from discord.ext import commands

minecraft_dir = '/home/artilapx/classic/'


def server_command(cmd):
    os.system('screen -S server -X stuff "{}\015"'.format(cmd))


def status():
    output = os.popen('screen -ls').read()
    if '.server' in output:
        print("Server is running.")
        return True
    else:
        print("Server is not running.")
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
            ctx.send("Сервер запущен.")
        else:
            ctx.send("Сервер уже запущен и работает.")


def setup(bot):
    bot.add_cog(Server(bot))
