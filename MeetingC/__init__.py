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

    agreements = [False, False]  # Booleans for agreement p1, p2, p3 and p4 TODO: [False, False, False, False]
    checkboxes = [False, False, False]  # Booleans for checkboxes choice_A, choice_B and choice_c

    @staticmethod
    def vars_for_template(player):
        """unique_a/b/c and shared_a/b/c provides the Project descriptions as strings"""
        #print(player.session.goal_matrix)
        # TODO: Logic is needed to provide the prefilled matrix

        return dict(  # individual project information as strings
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
        print(data['information'])
        if data['information'] == 'choice_A_selected':
            MeetingC.checkboxes = [True, False, False]
        if data['information'] == 'choice_B_selected':
            MeetingC.checkboxes = [False, True, False]
        if data['information'] == 'choice_C_selected':
            MeetingC.checkboxes = [False, False, True]

        # return the information of new selection to all players
        if data['information'] in ['choice_A_selected', 'choice_B_selected', 'choice_C_selected']:
            # set agreement to False
            MeetingC.agreements[0], MeetingC.agreements[1] = False, False
            # send the new input to webtemplate of all players
            return {0: dict(checkbox_update=data['information'], finished=False)}

        # Handle agreement
        # check if player1 agreed
        if data['information'] == 'p1_agreed':
            MeetingC.agreements[0] = True

        # check if player2 agreed
        if data['information'] == 'p2_agreed':
            MeetingC.agreements[1] = True

        # TODO: add if-statements for player 3 and 4

        # send information to web-template that the choice options shall be locked
        if data['information'] == 'locked':
            return {0: dict(locked=True)}

        # check if all players has agreed
        if MeetingC.agreements[0] and MeetingC.agreements[1]:  # MeetingC.agreements[2] and MeetingC.agreements[3]:
            if MeetingC.checkboxes == [False, False, False]:
                return {0: dict(finished=False)}
            else:
                return {0: dict(finished=True)}

    @staticmethod
    def before_next_page(player, timeout_happened):
        """click next  button -> store the final choice into the database"""
        print(MeetingC.checkboxes)
        if MeetingC.checkboxes[0]:
            player.final_choice = "Project A"
        if MeetingC.checkboxes[1]:
            player.final_choice = "Project B"
        if MeetingC.checkboxes[2]:
            player.final_choice = "Project C"



page_sequence = [MeetingC,]
