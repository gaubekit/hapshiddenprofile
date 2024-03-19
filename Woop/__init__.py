"""
Notes:
    - WOOP = Wish Outcome Obstacle Plan
    - All players do the WOOP-Task Individual Level
      Note: For Wish: Select two out of 8 (at the moment)

is Needed in Version:
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""


from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Woop'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    POSSIBLE_CHOICES = [
        dict(name='goal1', label="Goal1"),
        dict(name='goal2', label="Goal2"),
        dict(name='goal3', label="Goal3"),
        dict(name='goal4', label="Goal4"),
        dict(name='goal5', label="Goal5"),
        dict(name='goal6', label="Goal6"),
        dict(name='goal7', label="Goal7"),
        dict(name='goal8', label="Goal8"),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    goal1 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal2 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal3 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal4 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal5 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal6 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal7 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    goal8 = models.BooleanField(blank=True, null=True, field_maybe_none=True)


# PAGES
class ExplainWoopTask(Page):
    form_model = 'player'

class WoopTask(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [wish['name'] for wish in C.POSSIBLE_CHOICES]

    @staticmethod
    def error_message(player: Player, values):
        # print('values is', values)
        num_selected = 0
        for wish in C.POSSIBLE_CHOICES:
            if values[wish['name']]:
                num_selected += 1
        if num_selected != 2:
            return "You must select exactly 2 of the Options."

    @staticmethod
    def before_next_page(player: Player, **kwargs):
        # handle None Values
        if player.field_maybe_none('goal1') is None:
            player.goal1 = False
        if player.field_maybe_none('goal2') is None:
            player.goal2 = False
        if player.field_maybe_none('goal3') is None:
            player.goal3 = False
        if player.field_maybe_none('goal4') is None:
            player.goal4 = False
        if player.field_maybe_none('goal5') is None:
            player.goal5 = False
        if player.field_maybe_none('goal6') is None:
            player.goal6 = False
        if player.field_maybe_none('goal7') is None:
            player.goal7 = False
        if player.field_maybe_none('goal8') is None:
            player.goal8 = False


        # store the goals for the goal weighting in participants field
        participant = player.participant
        participant.goal_list = {'goal1':  player.goal1, 'goal2':  player.goal2,
                                 'goal3': player.goal3, 'goal4': player.goal4,
                                 'goal5':  player.goal5, 'goal6':  player.goal6,
                                 'goal7':  player.goal7, 'goal8':  player.goal8}


class FinishWoop(WaitPage):
   pass

page_sequence = [ExplainWoopTask, WoopTask, FinishWoop]
