from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

# InterventionA = Control; InterventionB = GoalSetting; InterventionC = GoalSetting + Spidergraph
SESSION_CONFIGS = [
    dict(name='Pilot', num_demo_participants=20, app_sequence=['Pilot']),
    #dict(name='InterventionA', num_demo_participants=2, app_sequence=[]),
    #dict(name='InterventionB', num_demo_participants=2, app_sequence=[]),
    dict(name='InterventionC', num_demo_participants=2, app_sequence=['Woop', 'Goalranking', 'Hiddenprofile', 'Projectbygoalindividual']) # 'Intro',
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

DEMO_PAGE_INTRO_HTML = ''

PARTICIPANT_FIELDS = ['goal_list',
                      'goal_ranking',
                      'unique_information',
                      'shared_information',
                      'ProjectA_list',
                      'ProjectV_list',
                      'ProjectC_list']

SESSION_FIELDS = ['chosen_goals',
                  'INFORMATION_A',
                  'INFORMATION_B',
                  'INFORMATION_C',
                  'test']

ROOMS = [dict(name='Test_session', display_name='Test_session')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


