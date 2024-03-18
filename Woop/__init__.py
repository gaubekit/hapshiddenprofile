"""
Notes:
    - WOOP = Wish Outcome Obstacle Plan
    - All players do the WOOP-Task Individual Level


    - player need to rank the importance of goals for the spidergraph..
      ..as part of spidergraph, it should maybe take place in the spidergraph part


is Needed in Version:
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""


from otree.api import *
from operator import itemgetter
import random


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

    first_goal_name = models.StringField()
    first_goal_rank = models.IntegerField(label="", min=1, max=5)
    second_goal_name = models.StringField()
    second_goal_rank = models.IntegerField(label="", min=1, max=5)
    third_goal_name = models.StringField()
    third_goal_rank = models.IntegerField(label="", min=1, max=5)
    fourth_goal_name = models.StringField()
    fourth_goal_rank = models.IntegerField(label="", min=1, max=5)


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

        participant = player.participant
        participant.goal_list = {'goal1':  player.goal1, 'goal2':  player.goal2,
                                 'goal3': player.goal3, 'goal4': player.goal4,
                                 'goal5':  player.goal5, 'goal6':  player.goal6,
                                 'goal7':  player.goal7, 'goal8':  player.goal8}


class WaitWoop(WaitPage):
  pass

# Note: Maybe a pass GoalWeigthing to the GoalRankingApp.
# If i do so, i should provide participant information about goal choice (true/false)

class GoalWeighting(Page):
    form_model = 'player'
    form_fields = ['first_goal_rank', 'second_goal_rank', 'third_goal_rank', 'fourth_goal_rank']

    @staticmethod
    def vars_for_template(player):
        goal_counts = {
            'goal1': 0, 'goal2': 0, 'goal3': 0, 'goal4': 0,
            'goal5': 0, 'goal6': 0, 'goal7': 0, 'goal8': 0
        }

        # count how often the goals were mentioned by the participants
        for p in player.subsession.get_players():
            for goal, count in goal_counts.items():
                goal_counts[goal] += getattr(p, goal)

        # separate named and unnamed goals
        goal_list = {goal: count for goal, count in goal_counts.items() if count != 0}
        unnamed_goals = {goal: count for goal, count in goal_counts.items() if count == 0}
        unnamed_goals = [goal for goal in unnamed_goals]

        # chose most mentioned goals
        sorted_goals = sorted(goal_list.items(), key=itemgetter(1), reverse=True)
        chosen_goals = [goal[0] for goal in sorted_goals[:4]]

        # fill up the goals up to four randomly, if there are less than four mentioned
        if len(chosen_goals) < 4:
            short_come = 4 - len(chosen_goals)
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


class FinishWoop(WaitPage):
    pass


page_sequence = [ExplainWoopTask, WoopTask, WaitWoop, GoalWeighting, FinishWoop]
