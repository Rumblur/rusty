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
            await ctx.send(f"Сервер запущен.")
        else:
            await ctx.send(f"Сервер уже запущен и работает.")

    @commands.command()
    async def start(self, ctx):
        """Останавливает сервер Minecraft."""
        if status():
            server_command('save-all')
            await ctx.send(f"Сохранение мира...")
            server_command('stop')
            await ctx.send(f"Остановка сервера...")
        else:
            await ctx.send(f"Сервер выключен.")


def setup(bot):
    bot.add_cog(Server(bot))
