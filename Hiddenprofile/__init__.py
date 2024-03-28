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

    INFORMATION_KEYS = ['human_resources', 'cost', 'duration', 'revenue', 'new_tech', 'social_benefits']

    @staticmethod
    def split_information(information_list: list, number_player: int):
        unique_information = random.sample(information_list, number_player) # TODO: Clarify -> should this be random?
        shared_information = [info for info in information_list if info not in unique_information]
        return unique_information, shared_information

    UNIQUE_INFORMATION_KEYS, SHARED_INFORMATION_KEYS = split_information(INFORMATION_KEYS, 2)

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

    individual_project_choice = models.StringField(choices=['Project A', 'Project B', 'Project C'],
                                                   label='Depending on the Information you have, which project would you choose?')

    ProjectA_human_resources = models.BooleanField(blank=True, initial=False)
    ProjectA_cost = models.BooleanField(blank=True, initial=False)
    ProjectA_duration = models.BooleanField(blank=True, initial=False)
    ProjectA_revenue = models.BooleanField(blank=True, initial=False)
    ProjectA_new_tech = models.BooleanField(blank=True, initial=False)
    ProjectA_social_benefits = models.BooleanField(blank=True, initial=False)
    #
    # ProjectB_human_resources
    # ProjectB_cost
    # ProjectB_duration
    # ProjectB_revenue
    # ProjectB_new_tech
    # ProjectB_social_benefits
    #
    # ProjectC_human_resources
    # ProjectC_cost
    # ProjectC_duration
    # ProjectC_revenue
    # ProjectC_new_tech
    # ProjectC_social_benefits
    #
    # vars_for_projectrating = [
    #     'ProjectA_human_resources', 'ProjectA_cost', 'PojectA_duration', 'PojectA_revenue', 'ProjectA_new_tech', 'ProjectA_social_benefits',
    #     'ProjectB_human_resources', 'ProjectB_cost', 'PojectC_duration', 'PojectC_revenue', 'ProjectC_new_tech','ProjectC_social_benefits',
    #     'ProjectC_human_resources', 'ProjectC_cost', 'PojectV_duration', 'PojectV_revenue', 'ProjectV_new_tech', 'ProjectV_social_benefits'
    # ]



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

        # store participant variables TODO: Question -> do i need this?
        player.participant.unique_information = player.unique_information
        player.participant.shared_information = player.shared_information

class RateProjects(Page):
    form_model = 'player'
    # form_fields = ['ProjectA_human_resources', 'ProjectA_cost','ProjectA_duration', 'ProjectA_revenue',
    #                'ProjectA_new_tech', 'ProjectA_social_benefits']

    @staticmethod
    def get_form_fields(player: Player):
        # Lists for checkboxes in Page RateProjects
        criteria_list_A = [f"ProjectA_{criteria}" for criteria in player.session.chosen_goals]
        projectA_criteria = [
            dict(name=criteria_list_A[0], label=f'{criteria_list_A[0]}'),
            dict(name=criteria_list_A[1], label=f'{criteria_list_A[1]}'),
            dict(name=criteria_list_A[2], label=f'{criteria_list_A[2]}'),
            dict(name=criteria_list_A[3], label=f'{criteria_list_A[3]}'),
            dict(name=criteria_list_A[4], label=f'{criteria_list_A[4]}'),]
        player.session.test = projectA_criteria

        # Note2me: used the participant field in for loop of the template
        player.participant.ProjectA_list = [crit['name'] for crit in projectA_criteria]
        #return player.participant.ProjectA_list
        return [crit['name'] for crit in projectA_criteria]

    @staticmethod
    def error_message(player: Player, values):
        print('values is', values)

    @staticmethod
    def before_next_page(player, timeout_happened):
        pass





# TODO: Note -> If we ask at this point to rank the goals depending on the provided Information (as shown in the MockUP)
#               the users could say only something about the information they have.. so each individual could rank the
#               projects by the two them given Information


class ResultsWaitPage(WaitPage):
     pass
#
#
# class Results(Page):
#     pass


page_sequence = [ProjectPitch, RateProjects]
