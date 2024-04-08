"""
Notes:
    - meetingA:
        ° jitsi in template
        ° box: showing individual information in separated Box -> via session and participant fields
        ° Team Choice Field with Timer #TODO Timer
        °
    - MeetingB (same as MeetingA instead of):
        ° access individual Project-Goal ranking TODO shift this to Premeeting
        ° compute joint project ranking  TODO shift this to Premeeting
        ° decision matrix goal/Project QUESTION: Same in InterventionB ??
        ° points without agreement has to be discussed in a first step TODO shift this to Premeeting


    - MeetingC (same as MeetingB instead of):
        ° Access ranked goals for spidergraph
        ° provide goal-ranking-information of all players for template/js
        ° show spidergraph

is Needed in Version:
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""


from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'MeetingC'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    final_choice = models.StringField()


# PAGES
class MeetingC(Page):
    # form_model = 'player'
    # form_fields = ['final_choice']

    @staticmethod
    def vars_for_template(player):
        """unique_a/b/c and shared_a/b/c provides the Project descriptions as strings"""
        #print(player.session.goal_matrix)
        # TODO: Logic is needed to provide the prefilled matrix

        # use this section to reset agreements and initialize choice checkboxes for live methode
        player.session.agreements = [False, False]  # Booleans for agreement p1, p2, p3 and p4 TODO: [False, False, False, False]
        player.session.checkboxes = [False, False, False]  # Booleans for checkboxes choice_A, choice_B and choice_c
        player.session.agree_count = 0

        return dict(  # Project Information
                    Information1=player.session.team_goal_matrix[0][0],
                    A1=player.session.team_goal_matrix[0][1],
                    B1=player.session.team_goal_matrix[0][2],
                    C1=player.session.team_goal_matrix[0][3],
                    Information2=player.session.team_goal_matrix[1][0],
                    A2=player.session.team_goal_matrix[1][1],
                    B2=player.session.team_goal_matrix[1][2],
                    C2=player.session.team_goal_matrix[1][3],
                    Information3=player.session.team_goal_matrix[2][0],
                    A3=player.session.team_goal_matrix[2][1],
                    B3=player.session.team_goal_matrix[2][2],
                    C3=player.session.team_goal_matrix[2][3],
                    Information4=player.session.team_goal_matrix[3][0],
                    A4=player.session.team_goal_matrix[3][1],
                    B4=player.session.team_goal_matrix[3][2],
                    C4=player.session.team_goal_matrix[3][3],
                    Information5=player.session.team_goal_matrix[4][0],
                    A5=player.session.team_goal_matrix[4][1],
                    B5=player.session.team_goal_matrix[4][2],
                    C5=player.session.team_goal_matrix[4][3],
                    Information6=player.session.team_goal_matrix[5][0],
                    A6=player.session.team_goal_matrix[5][1],
                    B6=player.session.team_goal_matrix[5][2],
                    C6=player.session.team_goal_matrix[5][3],
                      # individual project information as strings
                    unique_a=player.session.INFORMATION_A[player.participant.unique_information],
                    shared_a=player.session.INFORMATION_A[player.participant.shared_information],
                    unique_b=player.session.INFORMATION_B[player.participant.unique_information],
                    shared_b=player.session.INFORMATION_B[player.participant.shared_information],
                    unique_c=player.session.INFORMATION_C[player.participant.unique_information],
                    shared_c=player.session.INFORMATION_C[player.participant.shared_information])

    @staticmethod
    def js_vars(player):
        # store rankings of all players for visualization during jitsi-call
        return dict(one=player.session.team_goals[0],  # goal-rating of player1 (list of integers)
                    two=player.session.team_goals[1]  # goal-rating of player2
                    # TODO three=player.session.team_goals[2], four=player.session.team_goals[3]
                    )

    @staticmethod
    def live_method(player, data):
        #  Handle ticker across players -> update MeetingC-checkboxes if there inputs

        # print('input: ', data['information'])
        # print('checkbox: ', player.session.checkboxes)
        # print('agreements: ', player.session.agreements)
        if data['information'] == 'choice_A_selected':
            player.session.checkboxes = [True, False, False]
        if data['information'] == 'choice_B_selected':
            player.session.checkboxes = [False, True, False]
        if data['information'] == 'choice_C_selected':
            player.session.checkboxes = [False, False, True]

        # return the information of new selection to all players
        if data['information'] in ['choice_A_selected', 'choice_B_selected', 'choice_C_selected']:
            # set agreement to False
            player.session.agreements[0], player.session.agreements[1] = False, False
            player.session.agree_count = 0
            # send the new input to webtemplate of all players
            return {0: dict(checkbox_update=data['information'], finished=False, agreed=player.session.agree_count)}

        # Handle agreement
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
        if player.session.agreements[0] and player.session.agreements[1]:  # player.session.agreements[2] and player.session.agreements[3]:
            if player.session.checkboxes == [False, False, False]:
                return {0: dict(finished=False, agreed=player.session.agree_count)}
            else:
                print("TEST: ", player.session.checkboxes)
                return {0: dict(finished=True, agreed=player.session.agree_count)}
        else:
            return {0: dict(agreed=player.session.agree_count)}

    @staticmethod
    def before_next_page(player, timeout_happened):
        """click next  button -> store the final choice into the database"""
        print(player.session.checkboxes)
        if player.session.checkboxes[0]:
            player.final_choice = "Project A"
        if player.session.checkboxes[1]:
            player.final_choice = "Project B"
        if player.session.checkboxes[2]:
            player.final_choice = "Project C"


page_sequence = [MeetingC,]
