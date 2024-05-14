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


def make_field(label):
    return models.IntegerField(
        choices=[1,2,3,4,5,6,7],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    process_conflict = make_field('There were conflicts about people’s different ideas in the team.')

    relation_conflict1 = make_field('There was constant bickering in my team.')
    relation_conflict2 = make_field('People who offered new ideas in my team were likely to get clobbered.')
    relation_conflict3 = make_field('There were feelings among members of my team which tended to pull us apart')

    cooperation1 = make_field('Team members found it easy to work with each other.')
    cooperation2 = make_field('Team members were comfortable communicating with each other ')
    cooperation3 = make_field('Team members cooperated to get the work done')
    cooperation4 = make_field('Team members were very willing to share information with each other.')
    cooperation5 = make_field('Team members worked well together to make decisions.')


# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['process_conflict', 'relation_conflict1', 'relation_conflict2', 'relation_conflict3',
                   'cooperation1', 'cooperation2', 'cooperation3', 'cooperation4', 'cooperation5']


class ThankYou(Page):
    pass


page_sequence = [Questionnaire, ThankYou]
