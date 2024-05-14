
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
import numpy as np


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
        return [f'ProjectA_{player.participant.unique_information}', f'ProjectA_{player.participant.shared_information}',
                f'ProjectB_{player.participant.unique_information}', f'ProjectB_{player.participant.shared_information}',
                f'ProjectC_{player.participant.unique_information}', f'ProjectC_{player.participant.shared_information}']

    @staticmethod
    def vars_for_template(player):
        return dict(unique=player.participant.unique_information,
                    uniqueA=f'ProjectA_{player.participant.unique_information}',
                    uniqueB=f'ProjectB_{player.participant.unique_information}',
                    uniqueC=f'ProjectC_{player.participant.unique_information}',
                    shared=player.participant.shared_information,
                    sharedA=f'ProjectC_{player.participant.shared_information}',
                    sharedB=f'ProjectB_{player.participant.shared_information}',
                    sharedC=f'ProjectC_{player.participant.shared_information}')


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

        # fill combined matrix with player choices
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

        # deep copy of goal_matrix for further manipulation (find agreement in voting)
        player.session.team_goal_matrix = copy.deepcopy(player.session.goal_matrix)

        # print('goal_matrix:', player.session.goal_matrix)
        # print('team_goal_matrix:', player.session.team_goal_matrix)


class ProjectWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        """Calculate prefilled criteria-project-matrix"""

        # Note: Process just for one player, because if u process team_goal_matrix twice there will be a bias
        p_1 = group.get_players()[0]

        # find team goal agreement
        projects = {0: 'Project A', 1: 'Project B', 2: 'Project C'}
        goals_string = ''

        for goals in p_1.session.team_goal_matrix:

            i = 0
            for goal in goals[1:]:
                if goal == 0:
                    i += 1

            if i != 2:
                # set not agreed goals to 0, 0, 0
                goals[1], goals[2], goals[3] = 0, 0, 0
            else:
                # save name and project of goals with agreement
                for j, goal in enumerate(goals[1:]):
                    if goal != 0:
                        goals_string = f'{goals_string} <b>{goals[0]}: {projects[j]}</b> <br>'

        if goals_string == '':
            goals_string = 'there was no agreement in any points yet.'
        else:
            goals_string = 'your team agreed to the following:<br><br><p>' + goals_string[:-5] + '</p>'

        p_1.session.goals_string = goals_string
        p_1.session.team_goal_matrix = [[inner_list[0]] + [bool(value) for value in inner_list[1:]] for
                                           inner_list in p_1.session.team_goal_matrix]

        """ calculate overall team goal """  # TODO: i guess it could also be moved to goalranking
        # initialize lists for average of team goals inside a dict
        p_1.session.team_goals_avg = {}
        for i in range(5):
            p_1.session.team_goals_avg[p_1.session.goals[i]] = []

        # fill lists with ratings of all players
        for p in p_1.subsession.get_players():
            for i in range(5):
                # dict_team_goals[list_goal_names[goal_name]].append(dict_goal_rankings[list_goal_names[goal_name]])
                p.session.team_goals_avg[p.session.goals[i]].append(p.participant.goal_ranking[p.session.goals[i]])

        # overwrite the list inside the dict with the average of the players
        for i in range(5):
            p_1.session.team_goals_avg[p_1.session.goals[i]] = float(
                np.mean(np.array(p_1.session.team_goals_avg[p_1.session.goals[i]])))


page_sequence = [ProjectRating, ProjectWaitPage]
