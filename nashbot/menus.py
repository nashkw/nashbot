# menus.py


from random import shuffle
from discord import Embed
from emoji.core import emojize
from nashbot.varz import active_menus, STOP_EMOJI, BLANK
from nashbot.quotes import quizzes, opt_list, wrap, emoji_sets
from discord.ext.menus import MenuPages, Button, button, ListPageSource, Position, Last


def show_page_action(index):
    async def action(m, payload):
        await m.show_page(index)
    return action


def quiz_select_action(index):
    async def action(m, payload):
        question_no = m.current_page - 1
        if 0 <= question_no < len(m.questions) and index <= len(m.question_opts[question_no]):
            m.user_choices[question_no] = m.quiz[1][m.questions[question_no]][m.question_opts[question_no][index]]
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
                self.foots = ['(use the blue reaction emojis to navigate)' for p in pages]
            else:
                self.foots = [False for p in pages]
        elif isinstance(foots, str):
            self.foots = [foots for p in pages]
        else:
            self.foots = [f if f else '(use the blue reaction emojis to navigate)' for f in foots]

    async def format_page(self, m, page):
        if self.heads[m.current_page]:
            embed = Embed(title=self.name).add_field(name=self.heads[m.current_page], value=page)
        else:
            embed = Embed(title=self.name, description=page)
        if self.foots[m.current_page]:
            embed.set_footer(text=self.foots[m.current_page])
        return embed


class QuizSource(PSource):
    def __init__(self, name, description, questions, question_opts):
        pages = [BLANK + description + BLANK, *question_opts, 'end']
        foots = [False, *['(click the matching emoji to select an answer)' for q in questions], False]
        super().__init__(pages, wrap(name, 'grey_question'), heads=[False, *questions, False], foots=foots)

    async def format_page(self, m, to_display):
        print(f'formatting {to_display}')
        if to_display == 'end':
            self.heads[m.current_page] = BLANK + f'{m.get_num_answered()}/{len(m.questions)} questions answered'
            if m.is_quiz_completed():
                to_display = 'click the stop emoji to submit ur answers & get ur result!' + BLANK
            else:
                to_display = 'ur gonna need 2 go back & answer all the questions u skipped b4 u can submit' + BLANK
        elif isinstance(to_display, list):
            to_display = BLANK + opt_list(to_display, emojis=emoji_sets['fruit'])
        return await super().format_page(m, to_display)


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
        self.results = self.quiz[2]
        self.questions = list(self.quiz[1].keys())
        shuffle(self.questions)

        self.question_opts = []
        self.user_choices = []
        for q in self.questions:
            opts = list(self.quiz[1][q].keys())
            shuffle(opts)
            self.question_opts.append(opts)
            self.user_choices.append(None)

        source = QuizSource(quiz_name, self.quiz[0], self.questions, self.question_opts)
        super().__init__(source, **kwargs)
        max_emojis = max([len(opt) for opt in self.question_opts])
        for i, e in enumerate(emoji_sets['fruit'][:max_emojis]):
            self.add_button(Button(emojize(e, language='alias'), quiz_select_action(i), position=Last(2 + i)))

    def get_num_answered(self):
        return len([u_choice for u_choice in self.user_choices if u_choice is not None])

    def is_quiz_completed(self):
        return self.get_num_answered() >= len(self.questions)

    @button(STOP_EMOJI)
    async def stop_pages(self, payload):
        if self.is_quiz_completed():
            res = self.results[6]
            page = BLANK + res[2] + BLANK
            await self.change_source(PSource([page], self.source.name, heads=BLANK + wrap(res[0], res[1])))
        self.stop()

    async def finalize(self, timed_out):
        if self.is_quiz_completed():
            foot = '(type "quiz TODO" to take this quiz again)'
        else:
            foot = f'(this embed has {"timed out" if timed_out else "been deactivated"})'
        await self.change_source(PSource(self.source.entries, self.source.name, heads=self.source.heads, foots=foot))
        active_menus.remove(self)
