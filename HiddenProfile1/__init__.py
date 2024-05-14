""" hiddenprofile + projectbygoalindividual + preemeeting"""

from otree.api import *
import copy
import numpy as np


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'HiddenProfile1'
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
class ProjectRatingIndividual(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [f'ProjectA_{player.participant.unique_information}',
                f'ProjectA_{player.participant.shared_information}',
                f'ProjectB_{player.participant.unique_information}',
                f'ProjectB_{player.participant.shared_information}',
                f'ProjectC_{player.participant.unique_information}',
                f'ProjectC_{player.participant.shared_information}']

    @staticmethod
    def vars_for_template(player):
        return dict(
                    # unique and shared information used for matrix
                    unique=player.participant.unique_information,
                    uniqueA=f'ProjectA_{player.participant.unique_information}',
                    uniqueB=f'ProjectB_{player.participant.unique_information}',
                    uniqueC=f'ProjectC_{player.participant.unique_information}',
                    shared=player.participant.shared_information,
                    sharedA=f'ProjectC_{player.participant.shared_information}',
                    sharedB=f'ProjectB_{player.participant.shared_information}',
                    sharedC=f'ProjectC_{player.participant.shared_information}',

                    # individual project information as strings for hidden profile # TODO -> Note: Same as in MeetingC
                    unique_a=player.session.peaces_of_information[0][player.participant.unique_information],
                    shared_a=player.session.peaces_of_information[0][player.participant.shared_information],
                    unique_b=player.session.peaces_of_information[1][player.participant.unique_information],
                    shared_b=player.session.peaces_of_information[1][player.participant.shared_information],
                    unique_c=player.session.peaces_of_information[2][player.participant.unique_information],
                    shared_c=player.session.peaces_of_information[2][player.participant.shared_information]
        )

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
            return f"You have to choose exactly one project for {player.participant.unique_information}" \
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


class ProjectChoiceWaitPage(WaitPage):
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


class ProjectRatingTeam(Page):
    @staticmethod
    def vars_for_template(player):
        # initialize player.session.agreements for Agree button
        # Booleans for agreement p1, p2, p3 and p4 TODO: [False, False, False, False]
        player.session.agreements = [False, False]
        player.session.agree_count = 0

        return dict(
            # Project Information/Goals
            Information1=player.session.team_goal_matrix[0][0],
            Information2=player.session.team_goal_matrix[1][0],
            Information3=player.session.team_goal_matrix[2][0],
            Information4=player.session.team_goal_matrix[3][0],
            Information5=player.session.team_goal_matrix[4][0],
            Information6=player.session.team_goal_matrix[5][0],
            # individual project information as strings # TODO -> Note: Same as in MeetingC
            unique_a=player.session.peaces_of_information[0][player.participant.unique_information],
            shared_a=player.session.peaces_of_information[0][player.participant.shared_information],
            unique_b=player.session.peaces_of_information[1][player.participant.unique_information],
            shared_b=player.session.peaces_of_information[1][player.participant.shared_information],
            unique_c=player.session.peaces_of_information[2][player.participant.unique_information],
            shared_c=player.session.peaces_of_information[2][player.participant.shared_information])

    @staticmethod
    def live_method(player, data):
        # print(f"input for player {player.id_in_group}: ", data['information'])
        # print("team_goal_matrix: ", player.session.team_goal_matrix)

        if data['information'] == f'choice_A{1}_selected':
            player.session.team_goal_matrix[0][1:] = [True, False, False]
        if data['information'] == f'choice_B{1}_selected':
            player.session.team_goal_matrix[0][1:] = [False, True, False]
        if data['information'] == f'choice_C{1}_selected':
            player.session.team_goal_matrix[0][1:] = [False, False, True]

        # Information2
        if data['information'] == f'choice_A{2}_selected':
            # print(f'update {player.session.team_goal_matrix[1]} to ')
            player.session.team_goal_matrix[1][1:] = [True, False, False]
            # print(f'{player.session.team_goal_matrix[1][1:]}')
        if data['information'] == f'choice_B{2}_selected':
            player.session.team_goal_matrix[1][1:] = [False, True, False]
        if data['information'] == f'choice_C{2}_selected':
            player.session.team_goal_matrix[1][1:] = [False, False, True]

        # Information3
        if data['information'] == f'choice_A{3}_selected':
            player.session.team_goal_matrix[2][1:] = [True, False, False]
        if data['information'] == f'choice_B{3}_selected':
            player.session.team_goal_matrix[2][1:] = [False, True, False]
        if data['information'] == f'choice_C{3}_selected':
            player.session.team_goal_matrix[2][1:] = [False, False, True]

        # Information4
        if data['information'] == f'choice_A{4}_selected':
            player.session.team_goal_matrix[3][1:] = [True, False, False]
        if data['information'] == f'choice_B{4}_selected':
            player.session.team_goal_matrix[3][1:] = [False, True, False]
        if data['information'] == f'choice_C{4}_selected':
            player.session.team_goal_matrix[3][1:] = [False, False, True]

        # Information5
        if data['information'] == f'choice_A{5}_selected':
            player.session.team_goal_matrix[4][1:] = [True, False, False]
        if data['information'] == f'choice_B{5}_selected':
            player.session.team_goal_matrix[4][1:] = [False, True, False]
        if data['information'] == f'choice_C{5}_selected':
            player.session.team_goal_matrix[4][1:] = [False, False, True]

        # Information6
        if data['information'] == f'choice_A{6}_selected':
            player.session.team_goal_matrix[5][1:] = [True, False, False]
        if data['information'] == f'choice_B{6}_selected':
            player.session.team_goal_matrix[5][1:] = [False, True, False]
        if data['information'] == f'choice_C{6}_selected':
            player.session.team_goal_matrix[5][1:] = [False, False, True]

        # return the information of new selection to all players
        if data['information'] in ['choice_A1_selected', 'choice_B1_selected', 'choice_C1_selected',
                                   'choice_A2_selected', 'choice_B2_selected', 'choice_C2_selected',
                                   'choice_A3_selected', 'choice_B3_selected', 'choice_C3_selected',
                                   'choice_A4_selected', 'choice_B4_selected', 'choice_C4_selected',
                                   'choice_A5_selected', 'choice_B5_selected', 'choice_C5_selected',
                                   'choice_A6_selected', 'choice_B6_selected', 'choice_C6_selected']:
            # after a change set the agreement to False
            player.session.agreements[0], player.session.agreements[1] = False, False  # TODO 4 players
            # send the new input to webtemplate of all players
            player.session.agree_count = 0
            return {0: dict(checkbox_update=data['information'], finished=False, agreed=player.session.agree_count)}

        # handle agreement
        # check if player1 agreed
        if data['information'] == 'p1_agreed':
            player.session.agreements[0] = True
            player.session.agree_count = player.session.agreements[0] + player.session.agreements[1]

            # check if player2 agreed
        if data['information'] == 'p2_agreed':
            player.session.agreements[1] = True
            player.session.agree_count = player.session.agreements[0] + player.session.agreements[1]

            # TODO: add if-statements for player 3 and 4

        # send information to web-template that the choice options shall be locked
        if data['information'] == 'locked':
            return {0: dict(locked=True)}

        # check if all players has agreed
        if player.session.agreements[0] and player.session.agreements[
            1]:  # TODO and player.session.agreements[2] and player.session.agreements[3]:
            # print('BOTH AGREED')
            for i in range(0, 6):
                if player.session.team_goal_matrix[i][1:] == [False, False, False]:
                    return {0: dict(finished=False, agreed=player.session.agree_count)}

            print('all players agreed and checkboxes for all information are ticked')
            return {0: dict(finished=True, agreed=player.session.agree_count)}
        else:
            return {0: dict(agreed=player.session.agree_count)}

    @staticmethod
    def before_next_page(player, timeout_happened):
        # TODO: Which variables has to be stored for analysis?
        pass


page_sequence = [ProjectRatingIndividual, ProjectChoiceWaitPage, ProjectRatingTeam]
