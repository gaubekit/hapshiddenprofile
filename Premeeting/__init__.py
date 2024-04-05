from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Premeeting'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    offer_accepted = models.BooleanField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']

    @staticmethod
    def before_next_page(player, timeout_happened):
        for p in player.get_others_in_group():
            p.offer_accepted = True


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ]
