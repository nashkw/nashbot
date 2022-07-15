# menus.py


import discord
from discord.ext import menus
from nashbot.vars import active_menus


class MySource(menus.ListPageSource):
    def __init__(self, pages, title, header=None, footer=None):
        self.title = title
        self.head = header
        super().__init__(pages, per_page=1)
        if footer is None:
            self.foot = '(use the reaction emojis to navigate)' if self.is_paginating() else footer
        else:
            self.foot = footer

    async def format_page(self, menu, page):
        if self.head:
            embed = discord.Embed(title=self.title).add_field(name=self.head, value=page)
        else:
            embed = discord.Embed(title=self.title, description=page)
        if self.foot:
            embed.set_footer(text=self.foot)
        return embed


class MyMenuPages(menus.MenuPages):
    def __init__(self, bot_id, source, **kwargs):
        if source.is_paginating():
            active_menus.append(self)
        self.bot_id = bot_id
        super().__init__(source, **kwargs)

    def reaction_check(self, payload):
        if payload.user_id == self.bot_id and payload.event_type == 'REACTION_REMOVE':
            print('passed overriden check')
            return True
        return super().reaction_check(payload)

    async def finalize(self, timed_out):
        foot = f'(this embed has {"timed out" if timed_out else "been deactivated"})'
        await self.change_source(MySource(self.source.entries, self.source.title, header=self.source.head, footer=foot))
        active_menus.remove(self)