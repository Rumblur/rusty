import discord
from discord.ext import commands

import secret

client = commands.Bot(command_prefix=",")
client.remove_command('help')


@client.event
async def on_ready():
    print(client.user)
    print(client.user.id)


@client.command()
async def help(ctx, cmd=None):
    if cmd is None:
        emb = discord.Embed(description=f" **Информация**\n`help`, `status`", color=discord.Colour.blue())
        emb.set_author(name=f"Помощь прибыла!")
        emb.set_thumbnail(url=client.user.avatar_url)
        emb.set_footer(text=f"По запросу {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(description=f"Этой команды не существует.", color=discord.Colour.red())
        emb.set_author(name=f"Что-то пошло не так...")
        await ctx.send(embed=emb)


client.run(secret.secret)
