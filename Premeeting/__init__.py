"""
Notes:
    - video and audio check
    - instruction: preselected -> discuss points without agreement
    - compute agreement using player.session.goal_matrix -> update var
    - jitsi meeting in template
    - live methode: update table
is Needed in Version:
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
    - impactGoalSetting (goal-setting, normal jitsi)
"""


from otree.api import *



doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Premeeting'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class AudioVideoCheck(Page):
    # TODO add audio and video check
    # Note for Meeting A it has in the MeetingA App
    @staticmethod
    def before_next_page(player, timeout_happened):
        # find team goal agreement
        projects = {0: 'Project A', 1: 'Project B', 2: 'Project C'}

        goals_string = ''
        if player.id_in_group == 1:
            for goals in player.session.team_goal_matrix:

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
                            goals_string = goals_string + 'for ' + goals[0] + ' fits ' + projects[j] + ' best and '

            if goals_string == '':
                goals_string = 'The Team doesn\'t agree in any points yet. Please discuss them.'
            else:
                goals_string = 'Your team agreed that ' + goals_string[:-5] + '.'
            player.session.goals_string = goals_string
            print(player.session.goals_string)


class WaitCheckComplete(WaitPage):
    pass


class Discussion(Page):
    @staticmethod
    def vars_for_template(player):
        print("goalmatrix: ", player.session.goal_matrix)
        print("team_goal_matrix: ", player.session.team_goal_matrix)

        # initialize player.session.agreements for Agree button
        player.session.agreements = [False, False]  # Booleans for agreement p1, p2, p3 and p4 TODO: [False, False, False, False]

        return dict(  # individual project information as strings # TODO -> Note: Same as in MeetingC
            unique_a=player.session.INFORMATION_A[player.participant.unique_information],
            shared_a=player.session.INFORMATION_A[player.participant.shared_information],
            unique_b=player.session.INFORMATION_B[player.participant.unique_information],
            shared_b=player.session.INFORMATION_B[player.participant.shared_information],
            unique_c=player.session.INFORMATION_C[player.participant.unique_information],
            shared_c=player.session.INFORMATION_C[player.participant.shared_information])

    @staticmethod
    def live_method(player, data):

        for i in range(0, 6):
            # Information 1
            if data['information'] == f'choice_A{i+1}_selected':
                player.session.team_goal_matrix[i][1:] = [True, False, False]
            if data['information'] == f'choice_B{i+1}_selected':
                player.session.team_goal_matrix[i][1:] = [False, True, False]
            if data['information'] == f'choice_C{i+1}_selected':
                player.session.team_goal_matrix[i][1:] = [False, False, True]

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
                return {0: dict(checkbox_update=data['information'], finished=False)}

        # # Information 1
        # if data['information'] == 'choice_A1_selected':
        #     player.session.team_goal_matrix[0][1:] = [True, False, False]
        # if data['information'] == 'choice_B1_selected':
        #     player.session.team_goal_matrix[0][1:] = [False, True, False]
        # if data['information'] == 'choice_C1_selected':
        #     player.session.team_goal_matrix[0][1:] = [False, False, True]
        #
        # # return the information of new selection to all players
        # if data['information'] in ['choice_A1_selected', 'choice_B1_selected', 'choice_C1_selected']:
        #     # after a change set the agreement to False
        #     player.session.agreements[0], player.session.agreements[1] = False, False  # TODO 4 players
        #     # send the new input to webtemplate of all players
        #     return {0: dict(checkbox_update=data['information'], finished=False)}
        #
        # # Information 2
        # if data['information'] == 'choice_A2_selected':
        #     player.session.team_goal_matrix[1][1:] = [True, False, False]
        # if data['information'] == 'choice_B2_selected':
        #     player.session.team_goal_matrix[1][1:] = [False, True, False]
        # if data['information'] == 'choice_C2_selected':
        #     player.session.team_goal_matrix[1][1:] = [False, False, True]
        #
        # if data['information'] in ['choice_A2_selected', 'choice_B2_selected', 'choice_C2_selected']:
        #     player.session.agreements[0], player.session.agreements[1] = False, False  # TODO 4 players
        #     return {0: dict(checkbox_update=data['information'], finished=False)}
        #
        # # Information 3
        # if data['information'] == 'choice_A3_selected':
        #     player.session.team_goal_matrix[2][1:] = [True, False, False]
        # if data['information'] == 'choice_B3_selected':
        #     player.session.team_goal_matrix[2][1:] = [False, True, False]
        # if data['information'] == 'choice_C3_selected':
        #     player.session.team_goal_matrix[2][1:] = [False, False, True]
        #
        # if data['information'] in ['choice_A3_selected', 'choice_B3_selected', 'choice_C3_selected']:
        #     player.session.agreements[0], player.session.agreements[1] = False, False  # TODO 4 players
        #     return {0: dict(checkbox_update=data['information'], finished=False)}

        # TODO handle box changes
        # TODO handle agreement button
        # TODO handle next button

    @staticmethod
    def before_next_page(player, timeout_happened):
        pass


page_sequence = [AudioVideoCheck, WaitCheckComplete, Discussion, ]
