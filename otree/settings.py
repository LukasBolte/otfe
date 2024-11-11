from os import environ

SESSION_CONFIGS = [
    dict(
        name='otfe',
        app_sequence=['otfe'],
        num_demo_participants=6,
        development=False
    ),
    dict(
        name='otfe_dev',
        app_sequence=['otfe'],
        num_demo_participants=6,
        development=True
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0, doc=""
)

PARTICIPANT_FIELDS = ['treatment','start_time', 'end_time','finished','browser','cq_1_mistakes','cq_2_mistakes','attempts_training','attempts_work_1','attempts_work_2','attempts_work_3','which_belief','beliefs1','beliefs2','beliefs3','beliefs1_3','beliefs1_2','beliefs2_3','beliefs4','feedback','feedback_difficulty','feedback_understanding','feedback_satisfied','feedback_pay']
SESSION_FIELDS = ['prolific_completion_url']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6997314704613'
