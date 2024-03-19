"""
Notes:
    - access goals via participant
    - select common goals
    - weight common goals

is Needed in Version:
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
    SEED = random.randint(1, 500)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    first_goal_name = models.StringField()
    first_goal_rank = models.IntegerField(label="", min=1, max=5)
    second_goal_name = models.StringField()
    second_goal_rank = models.IntegerField(label="", min=1, max=5)
    third_goal_name = models.StringField()
    third_goal_rank = models.IntegerField(label="", min=1, max=5)
    fourth_goal_name = models.StringField()
    fourth_goal_rank = models.IntegerField(label="", min=1, max=5)

# PAGES

# Note: Testpage, excluded TODO: del
# class GoalRanking(Page):
    # @staticmethod
    # def vars_for_template(player):
    #     key_value = []
    #     for key, value in player.participant.goal_ranking.items():
    #         key_value.append((key, value))
    #
    #     return dict(test = key_value[0])
    # pass


class GoalWeighting(Page):
    form_model = 'player'
    form_fields = ['first_goal_rank', 'second_goal_rank', 'third_goal_rank', 'fourth_goal_rank']

    @staticmethod
    def vars_for_template(player):

        # setting a goal_count dict for counting goals mentioned
        goal_counts = {
            'goal1': 0, 'goal2': 0, 'goal3': 0, 'goal4': 0,
            'goal5': 0, 'goal6': 0, 'goal7': 0, 'goal8': 0
        }

        # count how often the goals were mentioned by the participants
        for p in player.subsession.get_players():
            for goal, count in goal_counts.items():
                # goal_counts[goal] += getattr(p, goal)
                goal_counts[goal] += p.participant.goal_list[goal]

        # separate named and unnamed goals
        goal_list = {goal: count for goal, count in goal_counts.items() if count != 0}
        unnamed_goals = {goal: count for goal, count in goal_counts.items() if count == 0}

        # chose most mentioned goals
        sorted_goals = sorted(goal_list.items(), key=itemgetter(1), reverse=True)
        chosen_goals = [goal[0] for goal in sorted_goals[:4]]

        unnamed_goals = [goal for goal in unnamed_goals if goal not in chosen_goals]

        # add goals by random, if there are less than 4 mentioned
        if len(chosen_goals) < 4:
            short_come = 4 - len(chosen_goals)
            random.seed(C.SEED)
            additional_goals = random.sample(unnamed_goals, short_come)
            chosen_goals.extend(additional_goals)

        player.first_goal_name = chosen_goals[0]
        player.second_goal_name = chosen_goals[1]
        player.third_goal_name = chosen_goals[2]
        player.fourth_goal_name = chosen_goals[3]

        return dict(first_goal=chosen_goals[0],
                    second_goal=chosen_goals[1],
                    third_goal=chosen_goals[2],
                    fourth_goal=chosen_goals[3]
                    )

    @staticmethod
    def js_vars(player: Player):
        return dict(first_goal_js=player.first_goal_name,
                    second_goal_js=player.second_goal_name,
                    third_goal_js=player.third_goal_name,
                    fourth_goal_js=player.fourth_goal_name
                    )

    @staticmethod
    def error_message(player: Player, values):
        num_selected = (values['first_goal_rank']
                        + values['second_goal_rank']
                        + values['third_goal_rank']
                        + values['fourth_goal_rank'])
        if num_selected > 15:
            return "Please make sure that you allocate a maximum of 15 points."

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.goal_ranking = {player.first_goal_name:  player.first_goal_rank,
                                    player.second_goal_name:  player.second_goal_rank,
                                    player.third_goal_name:  player.third_goal_rank,
                                    player.fourth_goal_name:  player.fourth_goal_rank}


class FinishGoalWeighting(WaitPage):
    pass


page_sequence = [GoalWeighting, FinishGoalWeighting]
