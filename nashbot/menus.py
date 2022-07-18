# menus.py


from discord import Embed
from nashbot.vars import active_menus
from discord.ext.menus import MenuPages, Button, button, ListPageSource, Position


class PSource(ListPageSource):
    def __init__(self, pages, title, headers=None, footer=None):
        self.name = title
        if headers is None:
            self.heads = [False for p in pages]
        else:
            self.heads = headers
        super().__init__(pages, per_page=1)
        if footer is None:
            self.foot = '(use the reaction emojis to navigate)' if self.is_paginating() else footer
        else:
            self.foot = footer

    async def format_page(self, m, page):
        if self.heads[m.current_page]:
            embed = Embed(title=self.name).add_field(name=self.heads[m.current_page], value=page)
        else:
            embed = Embed(title=self.name, description=page)
        if self.foot:
            embed.set_footer(text=self.foot)
        return embed


class MyMenuPages(MenuPages):
    def __init__(self, source, **kwargs):
        if source.is_paginating():
            active_menus.append(self)
        super().__init__(source, **kwargs)

    @button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def stop_pages(self, payload):
        self.stop()

    def reaction_check(self, payload):
        if payload.user_id == self.bot.user.id and payload.event_type == 'REACTION_REMOVE':
            return True
        return super().reaction_check(payload)

    async def finalize(self, timed_out):
        foot = f'(this embed has {"timed out" if timed_out else "been deactivated"})'
        await self.change_source(PSource(self.source.entries, self.source.name, headers=self.source.heads, footer=foot))
        active_menus.remove(self)


class HelpPages(MyMenuPages, inherit_buttons=False):
    def __init__(self, buttons, source, **kwargs):
        super().__init__(source, **kwargs)
        for b in buttons:
            self.add_button(Button(b[0], b[1], position=Position(b[2])))
