import asyncio
import os
import re

from discord.ext import commands

minecraft_dir = '/home/artilapx/minecraft/'

#  BadCoder thanks


def session_exists():
    return os.system("tmux has-session -t minecraft 2> /dev/null") == 0


def send_command(command):
    patched = re.sub(r"[^\w]", "\\\\\\g<0>", command, 0)
    os.system(f"tmux send-keys -t minecraft.0 {patched} ENTER")


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
            await ctx.send(f"`Отправлен запрос на включение сервера...`")
        else:
            await ctx.send(f"`Сервер уже запущен и работает. Запуск не требуется.`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        """Перезагружает сервер Rumblur."""
        if session_exists():
            os.system("mtc restart --now")
            await ctx.send(f"`Отправлен запрос на перезагрузку сервера...`")
        else:
            await ctx.send(f"`Сервер выключен. Нечего перезагружать.`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        """Останавливает сервер Rumblur."""
        if session_exists():
            os.system("mtc shutdown --confirm")
            await ctx.send(f"`Отправлен запрос на выключение сервера...`")
        else:
            await ctx.send(f"`Сервер уже выключен. Остановка не требуется.`")


def setup(bot):
    bot.add_cog(Server(bot))
