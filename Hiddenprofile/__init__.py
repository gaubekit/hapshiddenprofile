"""
Notes:
    - Page for introduction of the task
    - split the information to the participants (hardcoded p1 -  p4)


is Needed in Version:
    - control (no goal-setting, normal jitsi)
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""


from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Hiddenprofile'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SEED = random.randint(1, 500)

    # Note: maybe fit the possible Information with the Possible wishes.. so it had at the moment be 8
    INFORMATION_KEYS = ['human_resources', 'cost', 'duration', 'revenue', 'new_tech', 'social_benefits']

    @staticmethod
    def split_information(information_list: list, number_player: int):
        unique_information = random.sample(information_list, number_player) # TODO: Clarify -> should this be random?
        shared_information = [info for info in information_list if info not in unique_information]
        return unique_information, shared_information

    UNIQUE_INFORMATION_KEYS, SHARED_INFORMATION_KEYS = split_information(INFORMATION_KEYS, 2)

    # Todo: Replace placeholders with "real" information
    INFORMATION_A = {'human_resources': 'placeholder HUMAN RESOURCES information A',
                     'cost': 'placeholder COST information A',
                     'duration': 'placeholder DURATION information A',
                     'revenue': 'placeholder REVENUE information A',
                     'new_tech': 'placeholder NEW TECHNOLOGY information A',
                     'social_benefits': 'placeholder SOCIAL BENEFITS information A'}

    INFORMATION_B = {'human_resources': 'placeholder HUMAN RESOURCES information B',
                     'cost': 'placeholder COST information B',
                     'duration': 'placeholder DURATION information B',
                     'revenue': 'placeholder REVENUE information B',
                     'new_tech': 'placeholder NEW TECHNOLOGY information B',
                     'social_benefits': 'placeholder SOCIAL BENEFITS information B'}

    INFORMATION_C = {'human_resources': 'placeholder HUMAN RESOURCES information C',
                     'cost': 'placeholder COST information C',
                     'duration': 'placeholder DURATION information C',
                     'revenue': 'placeholder REVENUE information C',
                     'new_tech': 'placeholder NEW TECHNOLOGY information C',
                     'social_benefits': 'placeholder SOCIAL BENEFITS information C'}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    unique_information = models.StringField()
    shared_information = models.StringField()



# PAGES
class ProjectPitch(Page):
    """Every player should have some unique Information about the project"""
    @staticmethod
    def vars_for_template(player):
        for i, p in enumerate(player.subsession.get_players()):
            p.unique_information = C.UNIQUE_INFORMATION_KEYS[i]

            p.shared_information = C.SHARED_INFORMATION_KEYS[0]
            # TODO for 4 players use code below instead of line above
            # if i % 2 == 0:
            #     p.shared_information = C.SHARED_INFORMATION_KEYS[0]
            # else:
            #     p.shared_information = C.SHARED_INFORMATION_KEYS[1]


        return dict(information_A_1=C.INFORMATION_A[player.unique_information],
                    information_A_2=C.INFORMATION_A[player.shared_information],
                    information_B_1=C.INFORMATION_B[player.unique_information],
                    information_B_2=C.INFORMATION_B[player.shared_information],
                    information_C_1=C.INFORMATION_C[player.unique_information],
                    information_C_2=C.INFORMATION_C[player.shared_information])

    @staticmethod
    def before_next_page(player, durationout_happened):

        # store session variables
        player.session.INFORMATION_A = C.INFORMATION_A
        player.session.INFORMATION_B = C.INFORMATION_B
        player.session.INFORMATION_C = C.INFORMATION_C

        # store participant variables TODO: Question -> do i need this?
        player.participant.unique_information = player.unique_information
        player.participant.shared_information = player.shared_information


# TODO: Note -> If we ask at this point to rank the goals depending on the provided Information (as shown in the MockUP)
#               the users could say only something about the information they have.. so each individual could rank the
#               projects by the two them given Information

class ResultsWaitPage(WaitPage):
     pass
#
#
# class Results(Page):
#     pass


page_sequence = [ProjectPitch]
