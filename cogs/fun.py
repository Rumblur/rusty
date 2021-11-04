import aiohttp
import discord
from discord.ext import commands

sess = aiohttp.ClientSession()


class Fun(commands.Cog):
    """Фан-команды."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pat")
    @commands.guild_only()
    async def pat(self, ctx, users: commands.Greedy[discord.Member] = [], *, text: str = ""):
        """Погладить по голове. Использование: ,pat @mention"""
        resp = await sess.get("https://rra.ram.moe/i/r?type=pat")
        image_url = "https://rra.ram.moe" + (await resp.json())["path"]

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=f"**{discord.utils.escape_markdown(ctx.author.display_name)}** pats {', '.join(f'**{discord.utils.escape_markdown(u.display_name)}**' for u in users)} {text}"[
                  :256
                  ],
        )
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

    @commands.command(name="slap")
    @commands.guild_only()
    async def slap(self, ctx, users: commands.Greedy[discord.Member] = [], *, text: str = ""):
        """Шлёпнуть. Использование: ,slap @mention"""
        resp = await sess.get("https://rra.ram.moe/i/r?type=slap")
        image_url = "https://rra.ram.moe" + (await resp.json())["path"]

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=f"**{discord.utils.escape_markdown(ctx.author.display_name)}** slaps {', '.join(f'**{discord.utils.escape_markdown(u.display_name)}**' for u in users)} {text}"[
                  :256
                  ],
        )
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
