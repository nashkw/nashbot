# core.py


from os import environ, execv
from sys import argv, executable
from random import choice
from discord import Embed
from nashbot import quotes, read, varz
from discord.ext.commands import Cog, HelpCommand, command, is_owner


class Core(Cog, name='nashbot'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🛠'
        self.orig_help = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    async def safe_shutdown(self, ctx):
        if varz.active_menus:
            async with ctx.typing():
                while varz.active_menus:
                    varz.active_menus[0].stop()
                    await varz.active_menus[0].message.remove_reaction(varz.STOP_EMOJI, self.bot.user)
            await read.official(ctx, 'embeds deactivated', 'x')
        if ctx.voice_client is not None:
            await ctx.invoke(self.bot.get_command('clearqueue'))
        await read.official(ctx, '...shutting down...', 'zzz')

    @command(name='shutdown', aliases=['die', 'kys'], brief='shut down the bot', hidden=True,
             help='completely shut down the bot. it wont restart automatically afterwards so use w/ caution !!')
    @is_owner()
    async def shutdown(self, ctx):
        await read.quote(ctx, choice(await quotes.get_shutdown_quotes(ctx)))
        await self.safe_shutdown(ctx)
        await self.bot.close()

    @command(name='restart', aliases=['reboot', 'refresh'], brief='restart the bot',
             help='restart the bot. this will deactivate all embeds, clear all music queues, etc. use w/ caution !!')
    async def restart(self, ctx):
        await read.quote(ctx, choice(await quotes.get_restart_quotes(ctx)))
        await self.safe_shutdown(ctx)
        environ['restart'] = str(ctx.channel.id)
        execv(executable, ['python'] + argv)

    async def error_handling(self, ctx, error):
        return False

    def cog_unload(self):
        self.bot.help_command = self.orig_help


def setup(bot):
    bot.add_cog(Core(bot))


class CustomHelp(HelpCommand):

    def __init__(self):
        self.COG_HELP_FOOTER = '(for more information on a command try typing "help [commandname]")'
        cmd_attrs = {
            'brief': 'show this menu',
            'help': 'show a help menu with all the cmd categories, or a more specific help message if u requested smth',
            'aliases': ['helpme', 'sendhelp'],
            'extras': {'examples': ['help', 'sendhelp music', 'helpme vote']},
        }
        super().__init__(command_attrs=cmd_attrs)

    def page_tables(self, cmds):
        p_tables, cmds = '', [[c for c in cmds if not c.hidden], [c for c in cmds if c.hidden]]
        if cmds[0]:
            p_tables += quotes.get_table([[c, c.brief.lower()] for c in cmds[0]])
        if cmds[1]:
            p_tables += quotes.get_table([[c, c.brief.lower()] for c in cmds[1]])
        return p_tables

    def num_cmds(self, cmds):
        n_cmds, cmds = [], [[c for c in cmds if not c.hidden], [c for c in cmds if c.hidden]]
        if cmds[0]:
            n_cmds.append(quotes.add_s(f'{len(cmds[0])} command', cmds[0]))
        if cmds[1]:
            n_cmds.append(quotes.add_s(f'{len(cmds[1])} nash-only command', cmds[1]))
        return f'({", ".join(n_cmds)})'

    async def send_bot_help(self, mapping):
        title = quotes.wrap('nashbot™ commands & curios 4 all ur earthly needs', 'sparkles')
        buttons, pages, headers, footers = ['⏏️'], [varz.BLANK], ['command categories:'], [False]
        for cog, cmds in mapping.items():
            if cmds and cog:
                buttons.append(cog.emoji)
                pages.append(self.page_tables(cmds))
                headers.append(f'{cog.emoji}　**{cog.qualified_name}**　{self.num_cmds(cmds)}')
                footers.append(self.COG_HELP_FOOTER)
        pages[0] += quotes.opt_list(headers[1:])
        await read.help_paginated(self.context, buttons, title, pages, headers=headers, footers=footers)

    async def send_cog_help(self, cog):
        e = Embed(title=quotes.wrap(f'{cog.qualified_name} commands', cog.emoji, shorthand=False))
        e.add_field(name=self.num_cmds(cog.get_commands()), value=self.page_tables(cog.get_commands()) + '\n')
        e.set_footer(text=self.COG_HELP_FOOTER)
        await read.embed(self.get_destination(), e)

    async def send_command_help(self, cmd):
        explanation = varz.BLANK + cmd.help + varz.BLANK
        e = Embed(title=quotes.wrap(f'the {cmd} command', cmd.cog.emoji, shorthand=False), description=explanation)
        if cmd.aliases:
            e.add_field(name='other names for this command:', value='> ' + '\n> '.join(cmd.aliases) + varz.BLANK)
        if cmd.usage:
            examples = '\n'.join([f'> " {example} "' for example in cmd.usage]) + varz.BLANK
            e.add_field(name='examples of how to use this command: ', value=examples)
        if cmd.hidden:
            e.set_footer(text='(warning: this is a nash-only command, unusable by everyone else)')
        await read.embed(self.get_destination(), e)

