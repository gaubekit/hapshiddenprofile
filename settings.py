from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

# InterventionA = Control; InterventionB = GoalSetting; InterventionC = GoalSetting + Spidergraph
SESSION_CONFIGS = [
    dict(name='Pilot', num_demo_participants=20, app_sequence=['Pilot']),
    #dict(name='InterventionA', num_demo_participants=2, app_sequence=[]),
    #dict(name='InterventionB', num_demo_participants=2, app_sequence=['Premeeting', 'Intro']),
    dict(name='InterventionC', num_demo_participants=2, app_sequence=['Intro', 'Goalranking', 'Woop', 'Hiddenprofile', 'Projectbygoalindividual', 'Premeeting', 'MeetingC']), # 'Intro',
    dict(name='old_InterventionC', num_demo_participants=2, app_sequence=['Intro', 'old_Woop', 'old_Goalranking', 'Hiddenprofile', 'Projectbygoalindividual', 'Premeeting', 'MeetingC'])
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
                      'ProjectB_list',
                      'ProjectC_list',
                      ]

SESSION_FIELDS = ['goals',  # setup of all predefined (Intro) goals
                  'desc_pro_A',  # String describing Project A
                  'desc_pro_B',  # String describing Project B
                  'desc_pro_C',  # String describing Project C
                  'chosen_goals',
                  'team_goals',  # used for SpiderGraph during jitsi call
                  'INFORMATION_A',
                  'INFORMATION_B',
                  'INFORMATION_C',
                  'projectA_criteria',
                  'projectB_criteria',
                  'projectC_criteria',
                  'goal_matrix',
                  'team_goal_matrix',  # deep copy of goal_matrix for manipulation
                  'checkboxes',  # used to keep track of checkboxes in Meeting
                  'agreements',  # used to keep track of agreements in Meeting
                  'goals_string',  # save the pre-agreed goals
                  'agree_count'  # count how many players has actually agreed
                  ]

ROOMS = [dict(name='Test_session', display_name='Test_session')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


