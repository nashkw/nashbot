# menus.py


from random import shuffle
from discord import Embed
from emoji.core import emojize
from nashbot.varz import active_menus, STOP_EMOJI, BLANK
from nashbot.quotes import quizzes, opt_list, wrap, get_table
from discord.ext.menus import MenuPages, Button, button, ListPageSource, Position, Last


def show_page_action(index):
    async def action(m, payload):
        await m.show_page(index)
    return action


def quiz_select_action(index):
    async def action(m, payload):
        q_num = m.current_page - 1
        if 0 <= q_num < len(m.questions) and index <= len(m.question_opts[q_num]):
            if m.user_choices[q_num] == m.opts_meanings[q_num][index]:
                m.user_choices[q_num] = None
            else:
                m.user_choices[q_num] = m.opts_meanings[q_num][index]
            await m.show_current_page()
    return action


class PSource(ListPageSource):
    def __init__(self, pages, title, heads=None, foots=None, per_page=1):
        self.name = title
        super().__init__(pages, per_page=per_page)

        if heads is None:
            self.heads = [False for p in pages]
        elif isinstance(heads, str):
            self.heads = [heads for p in pages]
        else:
            self.heads = heads

        if foots is None:
            if self.is_paginating():
                self.foots = ['(use the blue reaction emojis to navigate)' for p in pages]
            else:
                self.foots = [False for p in pages]
        elif isinstance(foots, str):
            self.foots = [foots for p in pages]
        else:
            self.foots = [f if f else '(use the blue reaction emojis to navigate)' for f in foots]

    async def format_page(self, m, page):
        if isinstance(page, Embed):
            return page
        elif self.heads[m.current_page]:
            embed = Embed(title=self.name).add_field(name=self.heads[m.current_page], value=page)
        else:
            embed = Embed(title=self.name, description=page)
        if self.foots[m.current_page]:
            embed.set_footer(text=self.foots[m.current_page])
        return embed


class QuizSource(PSource):
    def __init__(self, info, questions, question_opts):
        self.emojis = info['emoji_set']
        pages = [BLANK + info['description'] + BLANK, *question_opts, 'end']
        foots = [False, *['(click the matching emoji to select an answer)' for q in questions], False]
        heads = [False, *[BLANK + q for q in questions], False]
        super().__init__(pages, wrap(info['name'], info['emoji']), heads=heads, foots=foots)

    async def format_page(self, m, to_display):
        if to_display == 'end':
            self.heads[m.current_page] = BLANK + f'{m.get_num_answered()}/{len(m.questions)} questions answered'
            if m.is_quiz_completed():
                to_display = 'click the stop emoji to submit ur answers & get ur result!' + BLANK
            else:
                to_display = 'ur gonna need 2 go back & answer all the questions u skipped b4 u can submit' + BLANK
        elif isinstance(to_display, list):
            q_num = m.current_page - 1
            if m.user_choices[q_num]:
                i = m.opts_meanings[q_num].index(m.user_choices[q_num])
                to_display = to_display.copy()
                to_display[i] = f'**{to_display[i]}**'
            to_display = BLANK + opt_list(to_display, emojis=self.emojis)
        return await super().format_page(m, to_display)


class Paginated(MenuPages):

    async def start(self, ctx, **kwargs):
        if self.source.is_paginating():
            active_menus.append(self)
        await super().start(ctx, **kwargs)

    def reaction_check(self, payload):
        if payload.user_id == self.bot.user.id and payload.event_type == 'REACTION_REMOVE':
            return True
        return super().reaction_check(payload)

    async def finalize(self, timed_out):
        foot = f'(this embed has {"timed out" if timed_out else "been deactivated"})'
        await self.change_source(PSource(self.source.entries, self.source.name, heads=self.source.heads, foots=foot))
        active_menus.remove(self)

    @button(STOP_EMOJI)
    async def stop_pages(self, payload):
        self.stop()


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
        self.info = quizzes[quiz_name][0]
        self.info['shortname'] = quiz_name
        self.questions = list(quizzes[quiz_name][1].keys())
        shuffle(self.questions)
        self.results = quizzes[quiz_name][2]

        self.question_opts = []
        self.opts_meanings = []
        self.user_choices = []
        for q in self.questions:
            opts = list(quizzes[quiz_name][1][q].keys())
            shuffle(opts)
            self.question_opts.append(opts)
            self.opts_meanings.append([quizzes[quiz_name][1][q][opt] for opt in opts])
            self.user_choices.append(None)

        super().__init__(QuizSource(self.info, self.questions, self.question_opts), **kwargs)
        max_emojis = max([len(opt) for opt in self.question_opts])
        for i, e in enumerate(self.info['emoji_set'][:max_emojis]):
            self.add_button(Button(emojize(e, language='alias'), quiz_select_action(i), position=Last(2 + i)))

    def get_num_answered(self):
        return len([u_choice for u_choice in self.user_choices if u_choice is not None])

    def is_quiz_completed(self):
        return self.get_num_answered() >= len(self.questions)

    def get_result(self, tally=None):
        if tally is None:
            tally = zip([sum(x) for x in zip(*self.user_choices)], self.results)
        tally = sorted(tally, reverse=True)
        table = get_table([[r[1][0], f'{round(100 * r[0]/self.info["max_result"])}%'] for r in tally], bords=False)
        result = tally[0][1]
        e = Embed(title=wrap(f"{self.ctx.author.name}'s {self.info['shortname']} quiz results", self.info['emoji']))
        e.add_field(name=BLANK + 'match percentages:', value=table + BLANK)
        e.add_field(name=BLANK + wrap(result[0], result[1]), value=BLANK + result[2] + BLANK)
        e.set_footer(text=f'(type "quiz {self.info["nickname"]}" if ud like 2 take this quiz again)')
        return e

    @button(STOP_EMOJI)
    async def stop_pages(self, payload):
        if self.is_quiz_completed():
            await self.change_source(PSource([self.get_result()], self.source.name))
        self.stop()
