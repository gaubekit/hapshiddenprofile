from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

# InterventionA = Control; InterventionB = GoalSetting; InterventionC = GoalSetting + Spidergraph
SESSION_CONFIGS = [
    # Pilot
    dict(name='Pilot', num_demo_participants=20, app_sequence=['Pilot']),
    # Control Group without GoalSetting/WOOP and adaptation
    dict(name='InterventionA', num_demo_participants=2, app_sequence=[   # TODO
        'Intro', 'Hiddenprofile', 'MeetingA', 'Outro']),
    # Intervention with GoalSetting/WOOP
    dict(name='InterventionB', num_demo_participants=2, app_sequence=[  # TODO
        'Intro', 'Goalranking', 'Woop', 'Hiddenprofile', 'Projectbygoalindividual', 'Premeeting', 'MeetingB', 'Outro']),
    # Intervention with GoalSetting/Woop as well as adaptation (Spidergraph)
    dict(name='InterventionC', num_demo_participants=2, app_sequence=[
        'Intro', 'Goalranking', 'Woop', 'Hiddenprofile', 'Projectbygoalindividual', 'Premeeting', 'MeetingC', 'Outro']),
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

DEMO_PAGE_INTRO_HTML = ''

PARTICIPANT_FIELDS = ['goal_ranking',  # stores the goal names as key and the related rating as value
                      'unique_information',  # Store for each player which unique piece of information he has
                      'shared_information',  # store for each player which shared piece of information he has
                      # TODO: try to replace functionality useing unique_information ect because it is just [f'{ProjectB_}participant.unique_information', f'{ProjectB_}participant.shared_information']
                      'ProjectA_list',
                      'ProjectB_list',
                      'ProjectC_list',
                      ]

SESSION_FIELDS = ['goals',  # setup of all predefined (Intro) goals
                  'desc_pro_A',  # String describing Project A
                  'desc_pro_B',  # String describing Project B
                  'desc_pro_C',  # String describing Project C
                  'team_goals_avg',  # new: used for SpiderGraph during jitsi call
                  'INFORMATION_A',  # dictionary with information of each criterion # TODO shorten (1dict), move to Intro, make keys independet of real information so we could change them
                  'INFORMATION_B',
                  'INFORMATION_C',
                  'goal_matrix',  # stores each Project-voting of each player for the criteria
                  'team_goal_matrix',  # deep copy of goal_matrix with binary information about agreement
                  'checkboxes',  # used to keep track of checkboxes in Meeting
                  'agreements',  # used to keep track of agreements in Meeting
                  'agree_count',  # count how many players has actually agreed to a decision
                  # TODO actually 'goals_string' it stores the Goals at strings, in future Version
                  #      this information should be used to prefill the matrix
                  'goals_string'  # save the pre-agreed goals
                  ]

ROOMS = [dict(name='Test_session', display_name='Test_session')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree'] #numpy


