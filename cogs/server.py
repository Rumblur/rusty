import asyncio
import os

from discord.ext import commands

minecraft_dir = '/home/artilapx/classic/'


def server_command(cmd):
    os.system(f'screen -S server -p 0 -X stuff "{cmd}^M"')


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
        """Запускает сервер Rumblur."""
        if not status():
            os.chdir(minecraft_dir)
            os.system('bash start.sh')
            await ctx.send(f"Запуск сервера...")
            await asyncio.sleep(10)
            await ctx.send(f"Сервер запущен.")
        else:
            await ctx.send(f"Сервер уже запущен и работает.")

    @commands.command()
    async def restart(self, ctx):
        """Перезагружает сервер Rumblur."""
        server_command('tellraw @a {\"text\":\"Перезагрузка через 30 секунд!\",\"color\":\"light_purple\"}')
        await ctx.send(f"Оповещение игроков. Перезагрузка через 30 секунд.")
        await asyncio.sleep(15)
        server_command(
            'tellraw @a {\"text\":\"Перезагрузка через 15 секунд! Началось сохранение...\",\"color\":\"light_purple\"}')
        await ctx.send(f"Оповещение игроков. Перезагрузка через 15 секунд. Сохранение через 5 секунд.")
        await asyncio.sleep(5)
        server_command('save-all')
        await ctx.send(f"Сохранение мира...")
        await asyncio.sleep(10)
        server_command('stop')
        await ctx.send(f"Остановка сервера...")
        await asyncio.sleep(15)
        os.chdir(minecraft_dir)
        os.system('bash start.sh')
        await ctx.send(f"Запуск сервера...")
        await asyncio.sleep(15)
        await ctx.send(f"Сервер запущен.")

    @commands.command()
    async def stop(self, ctx):
        """Останавливает сервер Rumblur."""
        if status():
            server_command('save-all')
            await ctx.send(f"Сохранение мира...")
            await asyncio.sleep(10)
            server_command('stop')
            await ctx.send(f"Остановка сервера...")
            await asyncio.sleep(10)
            await ctx.send(f"Сервер выключен.")
        else:
            await ctx.send(f"Сервер выключен.")


def setup(bot):
    bot.add_cog(Server(bot))
