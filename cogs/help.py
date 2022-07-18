# help.py


from discord import Embed
from nashbot import read, quotes
from discord.ext.commands import Cog, HelpCommand


class CustomHelp(HelpCommand):
    async def send_bot_help(self, mapping):
        embed = Embed(title=quotes.wrap('nashbot™ commands & curios 4 all ur earthly needs', 'sparkles'))
        for map_cog, map_cmds in mapping.items():
            if not (map_cog and map_cog.qualified_name == 'tests'):
                v = f"```\n{quotes.get_table([[cmd, cmd.help] for cmd in map_cmds if not cmd.hidden])}\n```"
                if map_cog:
                    embed.add_field(name=map_cog.qualified_name, value=v, inline=False)
                else:
                    embed.add_field(name='nashbot™', value=v.lower(), inline=False)
        await read.embed(self.get_destination(), embed)


class Help(Cog, name='help'):

    def __init__(self, bot):
        self.bot = bot
        self.orig_help = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    async def error_handling(self, ctx, error):
        return False

    def cog_unload(self):
        self.bot.help_command = self.orig_help


def setup(bot):
    bot.add_cog(Help(bot))

