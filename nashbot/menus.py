# menus.py


from random import shuffle
from discord import Embed
from emoji.core import emojize
from nashbot.varz import active_menus, STOP_EMOJI, BLANK
from nashbot.quotes import quizzes, opt_list, wrap, emoji_sets
from discord.ext.menus import MenuPages, Button, button, ListPageSource, Position, Last


def show_page_action(index):
    async def action(self_menu, payload):
        await self_menu.show_page(index)
    return action


class PSource(ListPageSource):
    def __init__(self, pages, title, heads=None, foots=None):
        self.name = title
        super().__init__(pages, per_page=1)

        if heads is None:
            self.heads = [False for p in pages]
        elif isinstance(heads, str):
            self.heads = [heads for p in pages]
        else:
            self.heads = heads

        if foots is None:
            if self.is_paginating():
                self.foots = ['(use the reaction emojis to navigate)' for p in pages]
            else:
                self.foots = [False for p in pages]
        elif isinstance(foots, str):
            self.foots = [foots for p in pages]
        else:
            self.foots = [f if f else '(use the reaction emojis to navigate)' for f in foots]

    async def format_page(self, m, page):
        if self.heads[m.current_page]:
            embed = Embed(title=self.name).add_field(name=self.heads[m.current_page], value=page)
        else:
            embed = Embed(title=self.name, description=page)
        if self.foots[m.current_page]:
            embed.set_footer(text=self.foots[m.current_page])
        return embed


class Paginated(MenuPages):
    def __init__(self, source, **kwargs):
        if source.is_paginating():
            active_menus.append(self)
        super().__init__(source, **kwargs)

    @button(STOP_EMOJI)
    async def stop_pages(self, payload):
        self.stop()

    def reaction_check(self, payload):
        if payload.user_id == self.bot.user.id and payload.event_type == 'REACTION_REMOVE':
            return True
        return super().reaction_check(payload)

    async def finalize(self, timed_out):
        foot = f'(this embed has {"timed out" if timed_out else "been deactivated"})'
        await self.change_source(PSource(self.source.entries, self.source.name, heads=self.source.heads, foots=foot))
        active_menus.remove(self)


class HelpPages(Paginated, inherit_buttons=False):
    def __init__(self, buttons, source, **kwargs):
        super().__init__(source, **kwargs)
        for i, b in enumerate(buttons):
            self.add_button(Button(b, show_page_action(i), position=Position(i)))

    @button(STOP_EMOJI, position=Last(0))
    async def stop_pages(self, payload):
        self.stop()


class QuizPages(Paginated):
    def __init__(self, quiz_name, **kwargs):
        self.quiz = quizzes[quiz_name]
        self.questions = list(self.quiz[1].keys())
        self.results = self.quiz[2]
        shuffle(self.questions)

        self.question_opts = []
        pages = [self.quiz[0]]
        foots = [False]
        for q in self.questions:
            opts = list(self.quiz[1][q].keys())
            shuffle(opts)
            self.question_opts.append(opts)
            pages.append(BLANK + opt_list(opts, emojis=emoji_sets['fruit']))
            foots.append('(click the matching emoji to select an answer)')

        source = PSource(pages, wrap(quiz_name, 'grey_question'), heads=[False, ] + self.questions, foots=foots)
        super().__init__(source, **kwargs)
        max_emojis = max([len(opt) for opt in self.question_opts])
        for i, e in enumerate(emoji_sets['fruit'][:max_emojis]):
            self.add_button(Button(emojize(e, language='alias'), show_page_action(i), position=Position(i)))

    @button(STOP_EMOJI, position=Last(2))
    async def stop_pages(self, payload):
        self.stop()
