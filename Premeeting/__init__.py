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
            """Process just for one player, because if u process team_goal_matrix twice there will be an bias"""
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

            print('original: ', player.session.goal_matrix)
            print('Team vorher: ', player.session.team_goal_matrix)
            player.session.team_goal_matrix = [[inner_list[0]] + [bool(value) for value in inner_list[1:]] for inner_list in player.session.team_goal_matrix]
            print('Team vorher: ', player.session.team_goal_matrix)


class WaitCheckComplete(WaitPage):
    pass


class Discussion(Page):
    @staticmethod
    def vars_for_template(player):
        # print("goalmatrix: ", player.session.goal_matrix)
        # print("team_goal_matrix: ", player.session.team_goal_matrix)

        # initialize player.session.agreements for Agree button
        player.session.agreements = [False, False]  # Booleans for agreement p1, p2, p3 and p4 TODO: [False, False, False, False]
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
            unique_a=player.session.INFORMATION_A[player.participant.unique_information],
            shared_a=player.session.INFORMATION_A[player.participant.shared_information],
            unique_b=player.session.INFORMATION_B[player.participant.unique_information],
            shared_b=player.session.INFORMATION_B[player.participant.shared_information],
            unique_c=player.session.INFORMATION_C[player.participant.unique_information],
            shared_c=player.session.INFORMATION_C[player.participant.shared_information])

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
            # return {0: dict(checkbox_update=data['information'], agreed=player.session.agree_count)}
            return {0: dict(checkbox_update=data['information'], finished=False, agreed=player.session.agree_count)}

        # handle agreement
        # check if player1 agreed
        if data['information'] == 'p1_agreed':
            player.session.agreements[0] = True
            player.session.agree_count = player.session.agreements[0]+player.session.agreements[1]

            # check if player2 agreed
        if data['information'] == 'p2_agreed':
            player.session.agreements[1] = True
            player.session.agree_count = player.session.agreements[0] + player.session.agreements[1]

            # TODO: add if-statements for player 3 and 4

        # send information to web-template that the choice options shall be locked
        if data['information'] == 'locked':
            return {0: dict(locked=True)}

        # check if all players has agreed
        if player.session.agreements[0] and player.session.agreements[1]:  # player.session.agreements[2] and player.session.agreements[3]:
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

page_sequence = [AudioVideoCheck, WaitCheckComplete, Discussion, ]
