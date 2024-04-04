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

    # INFORMATION_KEYS = ['human_resources', 'cost', 'duration', 'revenue', 'new_tech', 'social_benefits']
    #
    # @staticmethod
    # def split_information(information_list: list, number_player: int):
    #     unique_information = random.sample(information_list, number_player) # TODO: Clarify -> should this be random?
    #     shared_information = [info for info in information_list if info not in unique_information]
    #     return unique_information, shared_information
    #
    # UNIQUE_INFORMATION_KEYS, SHARED_INFORMATION_KEYS = split_information(INFORMATION_KEYS, 2)

    # Hardcoded uniqe and shared informations
    UNIQUE_INFORMATION_KEYS = ['human_resources', 'cost', 'duration', 'revenue']
    SHARED_INFORMATION_KEYS = ['new_tech', 'social_benefits']
    GOALS = UNIQUE_INFORMATION_KEYS+SHARED_INFORMATION_KEYS

    # Dictionarios containing information provided in the Page ProjectPitch
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

        # split shared and unique information to the players
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
    def before_next_page(player, timeout_happened):

        # store session variables
        player.session.INFORMATION_A = C.INFORMATION_A
        player.session.INFORMATION_B = C.INFORMATION_B
        player.session.INFORMATION_C = C.INFORMATION_C

        # store participant variables which are keys for session variables INFORMATION_A, _B and _C
        # TODO add further comments to make clear where and why this is needed
        player.participant.unique_information = player.unique_information
        player.participant.shared_information = player.shared_information
        # Note -> How to use: player.session.INFORMATION_C[player.participant.shared_information]

        # shared and unique player information
        information = [player.unique_information, player.shared_information]

        # Dictionarys withe names and labels for the formfields in ProjectRating, stored in session
        criteria_list_A = [f"ProjectA_{criteria}" for criteria in C.GOALS]
        projectA_criteria = [
            dict(name=f'{criteria_list_A[0]}', label=f'{criteria_list_A[0]}'),
            dict(name=f'{criteria_list_A[1]}', label=f'{criteria_list_A[1]}'),
            dict(name=f'{criteria_list_A[2]}', label=f'{criteria_list_A[2]}'),
            dict(name=f'{criteria_list_A[3]}', label=f'{criteria_list_A[3]}'),
            dict(name=f'{criteria_list_A[4]}', label=f'{criteria_list_A[4]}'),
            dict(name=f'{criteria_list_A[5]}', label=f'{criteria_list_A[5]}'),]

        # store the dictionary as projectA_criteria in session fields
        player.session.projectA_criteria = projectA_criteria
        # store a list of shared and unique- information names of the player
        player.participant.ProjectA_list = [crit for crit in criteria_list_A if crit[9:] in information]
        print('information: ', player.participant.ProjectA_list)

        # repeat for B
        # criteria_list_B = [f"ProjectB_{criteria}" for criteria in player.session.chosen_goals]
        criteria_list_B = [f"ProjectB_{criteria}" for criteria in C.GOALS]
        projectB_criteria = [
            dict(name=f'{criteria_list_B[0]}', label=f'{criteria_list_B[0]}'),
            dict(name=f'{criteria_list_B[1]}', label=f'{criteria_list_B[1]}'),
            dict(name=f'{criteria_list_B[2]}', label=f'{criteria_list_B[2]}'),
            dict(name=f'{criteria_list_B[3]}', label=f'{criteria_list_B[3]}'),
            dict(name=f'{criteria_list_B[4]}', label=f'{criteria_list_B[4]}'),
            dict(name=f'{criteria_list_B[5]}', label=f'{criteria_list_B[5]}'),]

        player.session.projectB_criteria = projectB_criteria
        player.participant.ProjectB_list = [crit for crit in criteria_list_B if crit[9:] in information]

        # repeat for C
        criteria_list_C = [f"ProjectC_{criteria}" for criteria in C.GOALS]
        projectC_criteria = [
            dict(name=f'{criteria_list_C[0]}', label=f'{criteria_list_C[0]}'),
            dict(name=f'{criteria_list_C[1]}', label=f'{criteria_list_C[1]}'),
            dict(name=f'{criteria_list_C[2]}', label=f'{criteria_list_C[2]}'),
            dict(name=f'{criteria_list_C[3]}', label=f'{criteria_list_C[3]}'),
            dict(name=f'{criteria_list_C[4]}', label=f'{criteria_list_C[4]}'),
            dict(name=f'{criteria_list_C[5]}', label=f'{criteria_list_C[5]}'),]

        player.session.projectC_criteria = projectC_criteria
        player.participant.ProjectC_list = [crit for crit in criteria_list_C if crit[9:] in information]

        # initialize goal matrix as session variable, is in downstream apps needed for the combined goal matrix
        player.session.goal_matrix = [
            ['human_resources', 0, 0, 0],
            ['cost', 0, 0, 0],
            ['duration', 0, 0, 0],
            ['revenue', 0, 0, 0],
            ['new_tech', 0, 0, 0],
            ['social_benefits', 0, 0, 0]
        ]



# TODO: Note -> If we ask at this point to rank the goals depending on the provided Information (as shown in the MockUP)
#               the users could say only something about the information they have.. so each individual could rank the
#               projects by the two them given Information


class ResultsWaitPage(WaitPage):
     pass



page_sequence = [ProjectPitch]
