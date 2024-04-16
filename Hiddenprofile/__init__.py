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

    # Hardcoded unique and shared information
    UNIQUE_INFORMATION_KEYS = ['human_resources', 'cost', 'duration', 'revenue']
    SHARED_INFORMATION_KEYS = ['new_tech', 'social_benefits']
    GOALS = UNIQUE_INFORMATION_KEYS+SHARED_INFORMATION_KEYS

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

        return dict(information_A_1=player.session.peaces_of_information[0][player.unique_information],
                    information_A_2=player.session.peaces_of_information[0][player.shared_information],
                    information_B_1=player.session.peaces_of_information[1][player.unique_information],
                    information_B_2=player.session.peaces_of_information[1][player.shared_information],
                    information_C_1=player.session.peaces_of_information[2][player.unique_information],
                    information_C_2=player.session.peaces_of_information[2][player.shared_information])

    @staticmethod
    def before_next_page(player, timeout_happened):

        # store unique and shared information in participant data
        player.participant.unique_information = player.unique_information
        player.participant.shared_information = player.shared_information

        # Note -> could be used like: player.session.peaces_of_information[0][player.participant.shared_information]

class ResultsWaitPage(WaitPage):
     pass

page_sequence = [ProjectPitch]
