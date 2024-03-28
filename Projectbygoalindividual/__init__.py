
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

    vars_for_projectrating = [
        ProjectA_human_resources, 'ProjectA_cost', 'PojectA_duration', 'PojectA_revenue', 'ProjectA_new_tech',
        'ProjectA_social_benefits',
        'ProjectB_human_resources', 'ProjectB_cost', 'PojectC_duration', 'PojectC_revenue', 'ProjectC_new_tech',
        'ProjectC_social_benefits',
        'ProjectC_human_resources', 'ProjectC_cost', 'PojectV_duration', 'PojectV_revenue', 'ProjectV_new_tech',
        'ProjectV_social_benefits'
    ]


# PAGES
class ProjectRatingPlayer1(Page):
    form_model = 'player'
    form_fields = vars_for_projectrating

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

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

    @staticmethod
    def error_message(player: Player, values):
        # print('values is', values)
        num_selected = 0
        for choice in C.POSSIBLE_CHOICES:
            if values[choice['name']]:
                num_selected += 1
        if num_selected != 2:
            return "You must select exactly 2 of the Options."


# class ResultsWaitPage(WaitPage):
#     pass
#
#
# class Results(Page):
#     pass


page_sequence = [MyPage]
