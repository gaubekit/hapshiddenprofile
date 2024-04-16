"""
Notes:
    - provide possible goals to players
    - player choice: most important goal for unspecific innovative projects
    - player goal rating, necessary for overall team goal
    - player could only continue to the next page if there is a goal chosen and a maximum of 18 points allocated

is Needed in Version:
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""

from otree.api import *
from operator import itemgetter
import random

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
    most_important_goal = models.StringField(initial='')
    goal_allocation_count = models.IntegerField(initial=0)
    first_goal_name = models.StringField()
    first_goal_rank = models.IntegerField(label="", min=1, max=5)
    second_goal_name = models.StringField()
    second_goal_rank = models.IntegerField(label="", min=1, max=5)
    third_goal_name = models.StringField()
    third_goal_rank = models.IntegerField(label="", min=1, max=5)
    fourth_goal_name = models.StringField()
    fourth_goal_rank = models.IntegerField(label="", min=1, max=5)
    fifth_goal_name = models.StringField()
    fifth_goal_rank = models.IntegerField(label="", min=1, max=5)
    sixth_goal_name = models.StringField()
    sixth_goal_rank = models.IntegerField(label="", min=1, max=5)


# PAGES

class GoalWeighting(Page):
    form_model = 'player'
    form_fields = ['first_goal_rank', 'second_goal_rank', 'third_goal_rank',
                   'fourth_goal_rank', 'fifth_goal_rank', 'sixth_goal_rank']

    @staticmethod
    def vars_for_template(player):
        # provide names of goals for formfields
        print(player.session.goals)
        player.first_goal_name = player.session.goals[0]
        player.second_goal_name = player.session.goals[1]
        player.third_goal_name = player.session.goals[2]
        player.fourth_goal_name = player.session.goals[3]
        player.fifth_goal_name = player.session.goals[4]
        player.sixth_goal_name = player.session.goals[5]

        return dict(first_goal=player.first_goal_name,
                    second_goal=player.second_goal_name,
                    third_goal=player.third_goal_name,
                    fourth_goal=player.fourth_goal_name,
                    fifth_goal=player.fifth_goal_name,
                    sixth_goal=player.sixth_goal_name)

    @staticmethod
    def js_vars(player: Player):
        # provide names to java, used in spider graph
        return dict(first_goal_js=player.session.goals[0],
                    second_goal_js=player.session.goals[1],
                    third_goal_js=player.session.goals[2],
                    fourth_goal_js=player.session.goals[3],
                    fifth_goal_js=player.session.goals[4],
                    sixth_goal_js=player.session.goals[5],
                    )

    @staticmethod
    def live_method(player, data):
        # update the most important goal
        if data['information'] in player.session.goals:
            player.most_important_goal = data['information']

        # update the total count
        if 'count' in data['information']:
            print('change in total count')
            player.goal_allocation_count = data['information']['count']
            print(player.id_in_group, player.goal_allocation_count)

        # condition for displaying next button
        if (len(player.most_important_goal) > 0) and (player.goal_allocation_count <= 18):
            return {player.id_in_group: dict(valid=True)}

        # condition for hiding next button
        if (len(player.most_important_goal) == 0) or (player.goal_allocation_count > 18):
            return {player.id_in_group: dict(valid=False)}

    @staticmethod
    def before_next_page(player, timeout_happened):
        """ store the goal-rankings in participant data"""
        participant = player.participant
        participant.goal_ranking = {'most_important_goal': player.most_important_goal,
                                    player.first_goal_name:  player.first_goal_rank,
                                    player.second_goal_name:  player.second_goal_rank,
                                    player.third_goal_name:  player.third_goal_rank,
                                    player.fourth_goal_name:  player.fourth_goal_rank,
                                    player.fifth_goal_name:  player.fifth_goal_rank,
                                    player.sixth_goal_name:  player.sixth_goal_rank}


class FinishGoalWeighting(WaitPage):
    pass


page_sequence = [GoalWeighting, FinishGoalWeighting]
