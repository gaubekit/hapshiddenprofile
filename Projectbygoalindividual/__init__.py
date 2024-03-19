
"""
Notes:
    - provide joint-project-goal-Matrix
    - individual Ranking of Project-goal Matrix  !!!
    - save information in Participant as Matrix



is Needed in Version:
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)

"""


from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Projectbygoalindividual'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(test=player.session.INFORMATION_C[player.participant.shared_information] )


# class ResultsWaitPage(WaitPage):
#     pass
#
#
# class Results(Page):
#     pass


page_sequence = [MyPage]
