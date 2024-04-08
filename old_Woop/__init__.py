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
    NAME_IN_URL = 'old_Woop'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    POSSIBLE_CHOICES = [
        dict(name='human_resources', label="need of human resources"),
        dict(name='cost', label="not that expensive"),
        dict(name='duration', label="short implementation time"),
        dict(name='revenue', label="generate revenue"),
        dict(name='new_tech', label="use of new technologie"),
        dict(name='social_benefits', label="social benefit"),
        # more goal's (fitting criteria) could be added
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    human_resources = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    cost = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    duration = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    revenue = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    new_tech = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    social_benefits = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    # goal7 = models.BooleanField(blank=True, null=True, field_maybe_none=True)
    # goal8 = models.BooleanField(blank=True, null=True, field_maybe_none=True)


# PAGES
class ExplainWoopTask(Page):
    form_model = 'player'

class WoopTask(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        #print([wish['name'] for wish in C.POSSIBLE_CHOICES])
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
        if player.field_maybe_none('human_resources') is None:
            player.human_resources = False
        if player.field_maybe_none('cost') is None:
            player.cost = False
        if player.field_maybe_none('duration') is None:
            player.duration = False
        if player.field_maybe_none('revenue') is None:
            player.revenue = False
        if player.field_maybe_none('new_tech') is None:
            player.new_tech = False
        if player.field_maybe_none('social_benefits') is None:
            player.social_benefits = False
        # if player.field_maybe_none('goal7') is None:
        #     player.goal7 = False
        # if player.field_maybe_none('goal8') is None:
        #     player.goal8 = False

        # store the goals for the goal weighting in participants field
        participant = player.participant
        participant.goal_list = {'human_resources':  player.human_resources, 'cost':  player.cost,
                                 'duration': player.duration, 'revenue': player.revenue,
                                 'new_tech':  player.new_tech, 'social_benefits':  player.social_benefits} #,
                                  #'goal7':  player.goal7, 'goal8':  player.goal8}


class FinishWoop(WaitPage):
   pass


page_sequence = [ExplainWoopTask, WoopTask, FinishWoop]
