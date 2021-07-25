import asyncio
import datetime
import time

import discord
from discord.ext import commands

import status
import secret

mss = status.Status()
bot = commands.Bot(command_prefix="/")

start_time = time.time()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def rusty(ctx):
    print(f'{ctx.message.author} has been used command rusty.')
    await ctx.channel.trigger_typing()
    help_embed = discord.Embed(title="Список команд Rusty",
                               description="Бот в разработке, поэтому список будет пополняться.", color=0x01579b)
    help_embed.set_thumbnail(
        url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/cat-face-with-wry-smile_1f63c.png")
    help_embed.add_field(name="Фановые команды:", value="/creeper - лучше не надо\n"
                                                        "/enchant <text> - зашифровать сообщение\n"
                                                        "/unenchant <text> - дешифровать сообщение\n"
                                                        "/villager <text> - переводчик на язык жителей\n",
                         inline=False)
    help_embed.add_field(name="Отладка:", value="/ping - задержка бота в мс\n"
                                                "/info - статистика\n",
                         inline=False)
    help_embed.set_footer(text="Information provided by Rusty",
                          icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
    await ctx.send(embed=help_embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def start(ctx):
    print(f'{ctx.message.author} has been used command start.')
    print('Starting monitoring Rumblur server...')
    mss.set_server_ip("rumblur.by")
    print('Monitoring started.')

    admin_channel = bot.get_channel(741254660026925147)

    if mss.get_server_ip() is None:
        return await ctx.send("Пожалуйста, укажите ip-адрес сервера.")
    try:
        mss.poll_server_status()
    except Exception as ex:
        print("Error: ", ex)

    message = await update_message(ctx)
    while True:
        try:
            mss.poll_server_status()
        except Exception as ex:
            print("Error: ", ex)
            crash_embed = discord.Embed(title="Сервер недоступен в данный момент.",
                                        description=f"Причина: {ex}",
                                        color=0xf44336)
            crash_embed.set_author(name="Having troubles...",
                                   icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/no-entry_26d4.png")
            crash_embed.set_thumbnail(
                url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/crying-cat-face_1f63f.png")
            crash_embed.set_footer(text="Information provided by Rusty",
                                   icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
            await admin_channel.send(embed=crash_embed)
        await update_message(ctx)

        await asyncio.sleep(60)


@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    print(f'Disabling bot...')
    await ctx.channel.trigger_typing()
    await ctx.send("Bye-bye!")
    await ctx.bot.logout()


async def update_message(ctx):
    server_status = mss.get_server_status()
    channel = bot.get_channel(741255934721916989)
    msg = await channel.fetch_message(808644874366746704)

    # CRASH
    crash_embed = discord.Embed(title="Сервер недоступен в данный момент.",
                                description="Если это происходит слишком часто, обратитесь к администрации сервера.",
                                color=0xf44336)
    crash_embed.set_author(name="Having troubles...",
                           icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/no-entry_26d4.png")
    crash_embed.set_thumbnail(
        url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/crying-cat-face_1f63f.png")
    crash_embed.set_footer(text="Information provided by Rusty",
                           icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
    # CRASH

    if server_status is None:
        if msg is not None:
            await msg.edit(embed=crash_embed)
        else:
            await ctx.send(embed=crash_embed)
    else:
        if server_status["update_flag"]:

            server_online_status = discord.Status.online
            if server_status['player_count'] == server_status['max_players']:
                server_online_status = discord.Status.do_not_disturb
            if int(server_status["player_count"]) == 0:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name="в пустоту")
            elif int(server_status["player_count"]) == 1:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name=f"за {server_status['player_count']} игроком")
            else:
                activity = discord.Activity(type=discord.ActivityType.watching,
                                            name=f"за {server_status['player_count']} игроками")

            await bot.change_presence(activity=activity, status=server_online_status)

            if int(server_status["player_count"]) > 0:
                num = 1
                player_names = "\n"
                for player in server_status["player_names"]:
                    player_names += str(num) + ". " + player + "\n"
                    num += 1
                player_names += ""
            else:
                player_names = "Никого нет на сервере..."

            server_online = "Онлайн"
            if server_status["version"] is None:
                server_online = "Неизвестно"

            # NEW
            new_embed = discord.Embed(title="Статистика сервера Rumblur", color=0x4caf50)
            new_embed.set_author(name="Rumblur Classic", url="https://rumblur.by",
                                 icon_url="https://rumblur.by/images/chainfire.png")
            new_embed.add_field(name="Статус", value=f"{server_online}", inline=True)
            new_embed.add_field(name="IP-адрес", value=f"{server_status['ip']}", inline=True)
            new_embed.add_field(name="Версия игры", value=f"{server_status['version']}", inline=True)
            new_embed.add_field(
                name=f"{server_status['player_count']} из " + f"{server_status['max_players']} игроков сейчас на сервере:",
                value=f"{player_names}", inline=True)
            new_embed.set_footer(text="Information provided by Rusty",
                                 icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
            # NEW

            # DEFAULT
            embed = discord.Embed(title="Статистика сервера Rumblur", color=0x4caf50)
            embed.set_author(name="Rumblur Classic", url="https://rumblur.by",
                             icon_url="https://rumblur.by/images/chainfire.png")
            embed.add_field(name="Статус", value=f"{server_online}", inline=True)
            embed.add_field(name="IP-адрес", value=f"{server_status['ip']}", inline=True)
            embed.add_field(name="Версия игры", value=f"{server_status['version']}", inline=True)
            embed.add_field(
                name=f"{server_status['player_count']} из " + f"{server_status['max_players']} игроков сейчас на сервере:",
                value=f"{player_names}", inline=True)
            embed.set_footer(text="Information provided by Rusty",
                             icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
            # DEFAULT

            if msg is not None:
                await msg.edit(content="Слежу за сервером...")
                await msg.edit(embed=new_embed)
            else:
                return await ctx.send(content="Слежу за сервером... ", embed=embed)


@bot.command()
async def ping(ctx):
    """Check ping of the bot"""
    print(f'{ctx.message.author} has been used command ping.')
    await ctx.channel.trigger_typing()
    latency = round(bot.latency * 1000)
    if latency <= 200:
        embed = discord.Embed(color=0x4caf50)
        embed.set_thumbnail(
            url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/grinning-cat-face-with-smiling-eyes_1f638.png")
        embed.add_field(name="Задержка бота Rusty", value=f"{latency} мс", inline=True)
        embed.set_footer(text="Information provided by Rusty",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
    elif 201 <= latency <= 500:
        embed = discord.Embed(color=0xffc107)
        embed.set_thumbnail(
            url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/pouting-cat-face_1f63e.png")
        embed.add_field(name="Задержка бота Rusty", value=f"{latency} мс", inline=True)
        embed.set_footer(text="Information provided by Rusty",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
    elif latency >= 501:
        embed = discord.Embed(color=0xf44336)
        embed.set_thumbnail(
            url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/weary-cat-face_1f640.png")
        embed.add_field(name="Задержка бота Rusty", value=f"{latency} мс", inline=True)
        embed.set_footer(text="Information provided by Rusty",
                         icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/paw-prints_1f43e.png")
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    """View statistics about the bot."""
    print(f'{ctx.message.author} has been used command info.')

    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(datetime.timedelta(seconds=difference))

    statics = (
        f"Время работы: `{uptime}`\n"
        f"Версия discord.py: `v{discord.__version__}`"
    )

    await ctx.channel.trigger_typing()

    embed = discord.Embed(title="Бот Rusty", color=0x039be5)
    embed.set_thumbnail(
        url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/google/3/cat_1f408.png")
    embed.add_field(name="Системная информация", value=statics, inline=True)
    embed.set_footer(
        text="1.2 | Created by Xtimms"
    )

    await ctx.send(embed=embed)


bot.run(secret.secret)
