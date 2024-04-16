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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    outcome = models.LongStringField(label='For the firm, an innovation project should...')
    obstacle = models.LongStringField(label='An obstacle in reality is ....')
    plan = models.LongStringField(label='If the obstacle occurs, then I will..')


class WoopTask(Page):
    form_model = 'player'
    form_fields = ['outcome', 'obstacle', 'plan']

    @staticmethod
    def vars_for_template(player):
        return dict(most_important_goal=player.participant.goal_ranking['most_important_goal'])


class FinishWoop(WaitPage):
   pass


page_sequence = [WoopTask, FinishWoop]
# page_sequence = [ExplainWoopTask, WoopTask, FinishWoop]
