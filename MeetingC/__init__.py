"""
Notes:
    - meetingA:
        ° jitsi in template
        ° box: showing individual information in separated Box --> need to accessed from Hiddenprofile
        ° Team Choice Field with Timer
        °
    - MeetingB (same as MeetingA instead of):
        ° access individual Project-Goal ranking
        ° compute joint project ranking
        ° decision matrix goal/Project QUESTION: Same in InterventionB ??

    - MeetingC (same as MeetingB instead of):
        ° Access ranked goals for spidergraph
        ° provide goal-ranking-information of all players for template/js
        ° show spidergraph





      ..points without agreement has to be discussed
      ..question: "agreement" meaning? most/all have the same idea?


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
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
