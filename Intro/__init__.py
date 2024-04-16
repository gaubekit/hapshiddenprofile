"""
Notes:
    - Giving general Information about experiment
    - collecting demographic data
    - set some participant and session variables, which are used later on

is Needed in Version:
    - control (no goal-setting, normal jitsi)
    - impactGoalSetting (goal-setting, normal jitsi)
    - impactGoalsSharedSetting (goal-setting, jitsi with intervention)
"""

from otree.api import *


doc = """
Giving Instructions about the Project and gathering general Participant-Information
"""


class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # demographics
    age = models.IntegerField(
        label='Age: ',
        min=16,
        max=99
    )

    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Diverse', 'Diverse']],
        label='Gender',
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class PreIntroduction(Page):
    # TODO maybe something necessary to handle the agreements

    @staticmethod
    def before_next_page(player, timeout_happened):
        """Store information about projects and goals in session variables"""
        # TODO: If change some goals or project(-information), do it here!

        # initialize predefined goals as session variable
        player.session.goals = [
            'human_resources', 'cost', 'duration',
            'revenue', 'new_tech', 'social_benefits'
        ]

        # Strings for Project information, accessed in template via {{ session.desc_pro_a }}
        player.session.desc_pro_A = 'Project A is a virtual reality fitness adventure game that combines immersive ' \
                                    + 'storytelling with physical exercise.<br>' \
                                    + 'Players embark on epic quests where they must complete fitness ' \
                                    + 'challenges to progress, making workouts engaging and rewarding.'

        player.session.desc_pro_B = 'Project B is an AI-powered shopping assistant that uses machine learning' \
                                    + ' algorithms to analyze user preferences, browsing history, and social media' \
                                    + ' data to provide personalized product recommendations and styling advice.'
        player.session.desc_pro_C = 'Project C is a smart home energy management system that integrates AI algorithms' \
                                    + ', IoT sensors, and user behavior analysis to optimize energy usage, ' \
                                    + 'reduce costs, and minimize environmental impact.'

        # List,storing dictionaries for Project A, B and C
        player.session.peaces_of_information = [
            # dictionary for Project A
            {'human_resources': 'placeholder HUMAN RESOURCES information A',
             'cost': 'placeholder COST information A',
             'duration': 'placeholder DURATION information A',
             'revenue': 'placeholder REVENUE information A',
             'new_tech': 'placeholder NEW TECHNOLOGY information A',
             'social_benefits': 'placeholder SOCIAL BENEFITS information A'},
            # dictionary for Project B
            {'human_resources': 'placeholder HUMAN RESOURCES information B',
             'cost': 'placeholder COST information B',
             'duration': 'placeholder DURATION information B',
             'revenue': 'placeholder REVENUE information B',
             'new_tech': 'placeholder NEW TECHNOLOGY information B',
             'social_benefits': 'placeholder SOCIAL BENEFITS information B'},
            # dictionary for Project C
            {'human_resources': 'placeholder HUMAN RESOURCES information C',
             'cost': 'placeholder COST information C',
             'duration': 'placeholder DURATION information C',
             'revenue': 'placeholder REVENUE information C',
             'new_tech': 'placeholder NEW TECHNOLOGY information C',
             'social_benefits': 'placeholder SOCIAL BENEFITS information C'}
        ]

        # initialize goal matrix with ['goal_name', 0, 0, 0] for each goal; is used in projectbygoalindividual
        player.session.goal_matrix = [
            [player.session.goals[0], 0, 0, 0],
            [player.session.goals[1], 0, 0, 0],
            [player.session.goals[2], 0, 0, 0],
            [player.session.goals[3], 0, 0, 0],
            [player.session.goals[4], 0, 0, 0],
            [player.session.goals[5], 0, 0, 0]
        ]


class Introduction(Page):
    pass


class ParticipantData(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class FinishIntro(WaitPage):
    pass


page_sequence = [PreIntroduction]
# page_sequence = [PreIntroduction, Introduction, ParticipantData, FinishIntro]
