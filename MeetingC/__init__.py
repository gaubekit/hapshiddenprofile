"""
Notes:
    - meetingA:
        ° jitsi in template
        ° box: showing individual information in separated Box -> via session and participant fields
        ° Team Choice Field with Timer
        °
    - MeetingB (same as MeetingA instead of):
        ° access individual Project-Goal ranking
        ° compute joint project ranking
        ° decision matrix goal/Project QUESTION: Same in InterventionB ??
        ° points without agreement has to be discussed in a first step

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
    pass


# PAGES
class MeetingC(Page):
    """ have to be a live page i guess
        - fist: """

    @staticmethod
    def vars_for_template(player):
        """unique_a/b/c and shared_a/b/c provides the Project descriptions as strings"""

        # TODO: Logic is needed to provide the prefilled matrix

        return dict(unique_a=player.session.INFORMATION_A[player.participant.unique_information],
                    shared_a=player.session.INFORMATION_A[player.participant.shared_information],
                    unique_b=player.session.INFORMATION_B[player.participant.unique_information],
                    shared_b=player.session.INFORMATION_B[player.participant.shared_information],
                    unique_c=player.session.INFORMATION_C[player.participant.unique_information],
                    shared_c=player.session.INFORMATION_C[player.participant.shared_information]
                    )
    @staticmethod
    def js_vars(player):
        # store rankings of all players for visualization during jitsi-call
        return dict(one=player.session.team_goals[0],  # goal-rating of player1 (list of integers)
                    two=player.session.team_goals[1]  # goal-rating of player2
                    )


page_sequence = [MeetingC,]
