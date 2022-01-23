import asyncio
import os

from discord.ext import commands

minecraft_dir = '/home/artilapx/minecraft/'

#  BadCoder thanks


def session_exists():
    return os.system("tmux has-session -t minecraft 2> /dev/null") == 0


def send_command(command):
    os.system(f"tmux send-keys -t minecraft.0 \"{command}\" ENTER")


def attach_session():
    os.system("tmux attach -t minecraft")


class Server(commands.Cog, command_attrs=dict(hidden=True), name="Server"):
    """Команды для взаимодействия с сервером Minecraft. Мы не можем их показать в целях безопасности."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start(self, ctx):
        """Запускает сервер Rumblur."""
        if not session_exists():
            os.system("mtc start --only")
            await ctx.send(f"`Запуск сервера...`")
            await asyncio.sleep(10)  # TODO Избавиться
            await ctx.send(f"`Сервер запущен.`")  # TODO Проверить исходя из состояния
        else:
            await ctx.send(f"`Сервер уже запущен и работает. Запуск не требуется.`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        """Перезагружает сервер Rumblur."""
        os.system("mtc restart --now")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        """Останавливает сервер Rumblur."""
        if session_exists():
            send_command("save-all")
            await ctx.send(f"`Сохранение мира...`")
            await asyncio.sleep(10)  # TODO Избавиться
            send_command("stop")
            await ctx.send(f"`Остановка сервера...`")
            await asyncio.sleep(10)  # TODO Избавиться
            await ctx.send(f"`Сервер выключен.`")
        else:
            await ctx.send(f"`Сервер уже выключен. Остановка не требуется.`")


def setup(bot):
    bot.add_cog(Server(bot))
