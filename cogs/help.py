import discord
from discord.ext import commands


class Help(commands.Cog):
    """Показывает сообщение, которое вы сейчас читаете."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *cog):
        """Показывает все модули бота."""
        if not cog:
            help_embed = discord.Embed(title='Доступные модули',
                                       description=f'Используйте команду `{ctx.prefix}help *название модуля*` чтобы узнать больше.',
                                       color=discord.Colour.blue())
            cogs_desc = ''
            for x in self.bot.cogs:
                cogs_desc += f'**{x}** - {self.bot.cogs[x].__doc__}\n'
            help_embed.add_field(name='\u200b',
                                 value=cogs_desc[0:len(cogs_desc) - 1] if cogs_desc[0:len(cogs_desc) - 1] else '\u200b',
                                 inline=False)
            await ctx.message.add_reaction(emoji='✉')
            await ctx.message.author.send(embed=help_embed)
        else:
            if len(cog) > 1:
                help_embed = discord.Embed(title='Ошибка.', description='Слишком много модулей.',
                                           color=discord.Color.red())
                await ctx.message.author.send(embed=help_embed)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            help_embed = discord.Embed(title=f'Команды модуля {cog[0]}',
                                                       description=self.bot.cogs[cog[0]].__doc__,
                                                       color=discord.Colour.blue())
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    help_embed.add_field(name=c.name, value=c.help, inline=False)
                            found = True
                if not found:
                    help_embed = discord.Embed(title='Ошибка.',
                                               description=f'Модуль "{cog[0]}" не существует.',
                                               color=discord.Color.red())
                else:
                    await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
