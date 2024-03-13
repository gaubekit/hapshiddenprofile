"""
This App is used for the pre-evaluation and is used in the associated session.
Research Purpose: gathering first information
"""

from otree.api import *

c = cu
doc = ''

class C(BaseConstants):
    NAME_IN_URL = 'Pilot'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    ProjectChoice = models.StringField(
        choices=[['Project A', 'Project A'], ['Project B', 'Project B'], ['Project C', 'Project C']],
        label='My choice of best project:',
        widget=widgets.RadioSelect)

    alignGoals = models.BooleanField(
        label='In choosing the best project, did you align yourself to the wishes or goals you set earlier?')

    woopUtility = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='To what extent were your wishes or goals helpful in choosing the best project?'
              ' (1: Not at all helpful; 5: highly helpful)',
        widget=widgets.RadioSelectHorizontal)

    Wish = models.LongStringField(label='An innovation project should...')

    Outcome = models.LongStringField(label='For the firm, an innovation project should...')

    Obstacle = models.LongStringField(label='An obstacle in reality is ....')

    Plan = models.LongStringField(label='If (obstacle A) occurs, then I will..')

    goalSatisfaction = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='To what extent were you satisfied with the process of defining your goals for an innovation project?'
              ' (1: not at all satisfied; 5: highly satisfied)',
        widget=widgets.RadioSelectHorizontal)

    projectChoiceSatisfaction = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='To what extent were you satisfied with the final choice of project?'
              ' (1: not at all satisfied; 5: highly satisfied)',
        widget=widgets.RadioSelectHorizontal)

    feedback = models.LongStringField(
        label='Any additional feedback or comments you would like to leave us?',
        blank=True)

    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Diverse', 'Diverse']],
        label='Gender',
        widget=widgets.RadioSelectHorizontal)

    Age = models.IntegerField(label='Age', max=99)

    decisionMaker = models.BooleanField(
        label='In your day to day work, are you confronted with the task of choosing between innovative projects to work on?',
        widget=widgets.RadioSelectHorizontal)

    frequencyDecisions = models.StringField(
        choices=[['Once a day', 'Once a day'], ['More than once a day', 'More than once a day'],
                 ['Once a week', 'Once a week'], ['More than once a week', 'More than once a week'],
                 ['Once a month', 'Once a month'], ['More than once a month', 'More than once a month'],
                 ['Once a quarter', 'Once a quarter'], ['More than once a quarter', 'More than once a quarter'],
                 ['Once a year', 'Once a year'], ['More than once a year', 'More than once a year'], ['Never', 'Never']],
        label='How often do you make decisions about projects (either for own work or for others to work on)?'
              ' Please choose the closest answer possible',
        widget=widgets.RadioSelect)

    countryOfResidence = models.StringField(label='Your country of residence')

    togetherWithColleague = models.BooleanField(
        label='In the past, did you make any of these decisions on projects together with your colleague(s)?',
        widget=widgets.RadioSelectHorizontal)

    # questions asked if togetherWithColleague ==  Yes
    existingProcess = models.StringField(
        label='Was there any process or method in choosing the best project? If so, please describe it.')

    # questions asked if togetherWithColleague ==  Yes
    satisfactionexistingProcess = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], [6, 'Not relevant']],
        label='How satisfied are you with the process of deciding the best project,'
              ' if any, in the past? (1: least satisfied; 5: most satisfied)',
        widget=widgets.RadioSelectHorizontal)

    # questions asked if togetherWithColleague ==  Yes
    digitalTools = models.StringField(
        label='What digital tools, if any, did you use, for making these decisions collaboratively?')

    contact = models.StringField(
        blank=True,
        label='If you would like to receive further updates on this research, please leave your e-mail address for future contact.')

    numEmployees = models.IntegerField(label='Number of employees in your organization (approximate number)')

    teamSize = models.IntegerField(label='Number of members in your team')

    likeabilityWoop = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='On a scale of 1 to 5, please rate how interesting the WOOP goal-setting method was to you,'
              ' to identify your goals for an innovation project? (1: least interesting; 5: most interesting)',
        widget=widgets.RadioSelectHorizontal)

    likelyToUseWoopInd = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='On a scale of 1 to 5, please rate how likely you are to use the WOOP goal-setting method,'
              ' in choosing your projects?(1: least likely; 5: most likely to use)',
        widget=widgets.RadioSelectHorizontal)

    likelyToUseWoopTeam = models.IntegerField(
        choices=[[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
        label='On a scale of 1 to 5, please rate how likely you are to use the WOOP goal-setting method,'
              ' in choosing your projects?(1: least likely; 5: most likely to use)',
        widget=widgets.RadioSelectHorizontal)

    decisiveElementWish = models.LongStringField(label='Was there any aspect of your wish that influenced your decision?')

    decisiveElementOutcome = models.LongStringField(label='Was there any aspect of your desired outcome that influenced your choice?')

    decisiveElementObstacle = models.LongStringField(label='Was there any aspect of your desired obstacle that influenced your choice?')

    decisiveElementPlan = models.LongStringField(label='Was there any aspect of your desired plan that influenced your choice?')



class PreIntroduction(Page):
    form_model = 'player'

class Introduction(Page):
    form_model = 'player'

class GeneralInformation(Page):
    form_model = 'player'
    form_fields = ['gender', 'Age', 'decisionMaker', 'frequencyDecisions', 'countryOfResidence', 'togetherWithColleague',
                      'numEmployees', 'teamSize']

class GeneralInformationExtended(Page):
    form_model = 'player'
    form_fields = ['existingProcess', 'satisfactionexistingProcess', 'digitalTools']

    def is_displayed(self):
        return self.togetherWithColleague is True

class WoopTask(Page):
    form_model = 'player'
    form_fields = ['Wish', 'Outcome', 'Obstacle', 'Plan']

class ProjectInformation(Page):
    form_model = 'player'
    form_fields = ['ProjectChoice', 'decisiveElementWish', 'decisiveElementOutcome', 'decisiveElementObstacle', 'decisiveElementPlan']

class Reflection(Page):
    form_model = 'player'
    form_fields = ['alignGoals', 'woopUtility', 'goalSatisfaction', 'projectChoiceSatisfaction', 'feedback', 'likelyToUseWoopInd', 'likeabilityWoop', 'likelyToUseWoopTeam']

class Contact(Page):
    form_model = 'player'
    form_fields = ['contact']

class Thankyou(Page):
    form_model = 'player'


page_sequence = [PreIntroduction, Introduction, GeneralInformation, GeneralInformationExtended, WoopTask,
                 ProjectInformation, Reflection, Contact, Thankyou]