"""
Notes:
    - Giving general Information about experiment
    - collecting basic Data (individual/player-level) for all sessions -> participant
    -

is Needed in Version:
    - control (no goal-setting, normal jitsi)
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""

from otree.api import *


doc = """
Giving Instructions about the Project and gathering general Participant-Information
"""


class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # demographics
    age = models.IntegerField(
        label='Age: ',
        min=16,
        max=99
    )

    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Diverse', 'Diverse']],
        label='Gender',
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class PreIntroduction(Page):
    form_model = 'player'

class Introduction(Page): # TODO: not includet in page_sequence yet
    form_model = 'player'

class ParticipantData(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']

class FinishIntro(WaitPage):
    pass




page_sequence = [PreIntroduction, ParticipantData, FinishIntro]
