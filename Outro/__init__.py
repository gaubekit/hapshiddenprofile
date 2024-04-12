"""
Notes:
    - follow-up questions TODO: To be defined
    - feedback

is Needed in Version:
    TODO: Maybe three versions needed because there are questions concerning the woop or spidergraph which make no sense in control...
          ..or set a variable in session field, storing the version to control page content
    - control (no goal-setting, normal jitsi)
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""


from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Questionnaire(Page):
    pass


class ThankYou(Page):
    pass


page_sequence = [Questionnaire, ThankYou]
