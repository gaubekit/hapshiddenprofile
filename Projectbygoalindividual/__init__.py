
"""
Notes:
    - provide joint-project-goal-Matrix
    - individual Ranking of Project-goal Matrix  !!!
    - save information in Participant as Matrix



is Needed in Version:
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)

"""


from otree.api import *
import copy


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Projectbygoalindividual'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ProjectA_human_resources = models.BooleanField(blank=True, initial=False)
    ProjectA_cost = models.BooleanField(blank=True, initial=False)
    ProjectA_duration = models.BooleanField(blank=True, initial=False)
    ProjectA_revenue = models.BooleanField(blank=True, initial=False)
    ProjectA_new_tech = models.BooleanField(blank=True, initial=False)
    ProjectA_social_benefits = models.BooleanField(blank=True, initial=False)

    ProjectB_human_resources = models.BooleanField(blank=True, initial=False)
    ProjectB_cost = models.BooleanField(blank=True, initial=False)
    ProjectB_duration = models.BooleanField(blank=True, initial=False)
    ProjectB_revenue = models.BooleanField(blank=True, initial=False)
    ProjectB_new_tech = models.BooleanField(blank=True, initial=False)
    ProjectB_social_benefits = models.BooleanField(blank=True, initial=False)

    ProjectC_human_resources = models.BooleanField(blank=True, initial=False)
    ProjectC_cost = models.BooleanField(blank=True, initial=False)
    ProjectC_duration = models.BooleanField(blank=True, initial=False)
    ProjectC_revenue = models.BooleanField(blank=True, initial=False)
    ProjectC_new_tech = models.BooleanField(blank=True, initial=False)
    ProjectC_social_benefits = models.BooleanField(blank=True, initial=False)


# PAGES


class ProjectRating(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return player.participant.ProjectA_list + player.participant.ProjectB_list + player.participant.ProjectC_list

    @staticmethod
    def vars_for_template(player):
        return dict(unique=player.participant.unique_information,
                    uniqueA=player.participant.ProjectA_list[0],
                    uniqueB=player.participant.ProjectB_list[0],
                    uniqueC=player.participant.ProjectC_list[0],
                    shared=player.participant.shared_information,
                    sharedA=player.participant.ProjectA_list[1],
                    sharedB=player.participant.ProjectB_list[1],
                    sharedC=player.participant.ProjectC_list[1])


    @staticmethod
    def error_message(player: Player, values):
        """there should be just one project choice per goal"""

        unique_goal_sel = (values[f'ProjectA_{player.participant.unique_information}']
                           + values[f'ProjectB_{player.participant.unique_information}']
                           + values[f'ProjectC_{player.participant.unique_information}'])

        shared_goal_sel = (values[f'ProjectA_{player.participant.shared_information}']
                           + values[f'ProjectB_{player.participant.shared_information}']
                           + values[f'ProjectC_{player.participant.shared_information}'])

        if unique_goal_sel != 1 and shared_goal_sel != 1:
            return f"You have to choose exactly one project for {player.participant.unique_information}"\
                   + f" and one for {player.participant.shared_information}!"

        if unique_goal_sel != 1:
            return f"You have to choose exactly one project for {player.participant.unique_information}!"

        if shared_goal_sel != 1:
            return f"You have to choose exactly one project for {player.participant.shared_information}!"

    @staticmethod
    def before_next_page(player, timeout_happened):
        """handle variables for other apps"""  # TODO -> clarify: wird diese app vor allen apps die die variable brauchen aufgerufen?

        # TODO: Doesn't work in new version because chosen_goals arent defined. Are the goals all ready stored?
        #       replaced by team_goals_avg
        # if player.id_in_group == 1:
        #     team_goals = []
        #     # does this work?
        #     for p in player.subsession.get_players(): # TODO rename to goals_of_team_members
        #         team_goals.append(
        #             [p.participant.goal_ranking[p.session.goals[0]],
        #              p.participant.goal_ranking[p.session.goals[1]],
        #              p.participant.goal_ranking[p.session.goals[2]],
        #              p.participant.goal_ranking[p.session.goals[3]],
        #              p.participant.goal_ranking[p.session.goals[4]],
        #              p.participant.goal_ranking[p.session.goals[5]]]
        #         )
        #
        #     player.session.team_goals = team_goals  # used in MeetingC store rankings of all players for visualization during jitsi-call

        # fill combined matrix with player choices
        # TODO -> Note: No changes after adjustment
        # human resources
        player.session.goal_matrix[0][1] += player.ProjectA_human_resources
        player.session.goal_matrix[0][2] += player.ProjectB_human_resources
        player.session.goal_matrix[0][3] += player.ProjectC_human_resources

        # cost
        player.session.goal_matrix[1][1] += player.ProjectA_cost
        player.session.goal_matrix[1][2] += player.ProjectB_cost
        player.session.goal_matrix[1][3] += player.ProjectC_cost

        # duration
        player.session.goal_matrix[2][1] += player.ProjectA_duration
        player.session.goal_matrix[2][2] += player.ProjectB_duration
        player.session.goal_matrix[2][3] += player.ProjectC_duration

        # revenue
        player.session.goal_matrix[3][1] += player.ProjectA_revenue
        player.session.goal_matrix[3][2] += player.ProjectB_revenue
        player.session.goal_matrix[3][3] += player.ProjectC_revenue

        # new tech
        player.session.goal_matrix[4][1] += player.ProjectA_new_tech
        player.session.goal_matrix[4][2] += player.ProjectB_new_tech
        player.session.goal_matrix[4][3] += player.ProjectC_new_tech

        # social benefits
        player.session.goal_matrix[5][1] += player.ProjectA_social_benefits
        player.session.goal_matrix[5][2] += player.ProjectB_social_benefits
        player.session.goal_matrix[5][3] += player.ProjectC_social_benefits

        # deep copy for manipulation
        player.session.team_goal_matrix = copy.deepcopy(player.session.goal_matrix)
        #print('team goals:', player.session.team_goals)
        print('goal_matrix:', player.session.goal_matrix)
        print('team_goal_matrix:', player.session.team_goal_matrix)


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [ProjectRating, ResultsWaitPage]
