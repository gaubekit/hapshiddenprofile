"""
Notes:
    - for the moment just test reasons
    - access goals via participant
    - weight it

is Needed in Version:
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""

from otree.api import *

doc = """
Your app description
""" #TODO


class C(BaseConstants):
    NAME_IN_URL = 'Goalranking'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

# PAGES
class GoalRanking(Page): #TODO: Learning how to acces values across apps --> use this to split goal selection into this app
    @staticmethod
    def vars_for_template(player):
        key_value = []
        for key, value in player.participant.goal_ranking.items(): # ToDo see this example
            key_value.append((key, value))

        return dict(test = key_value[0])


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [GoalRanking, ResultsWaitPage]
