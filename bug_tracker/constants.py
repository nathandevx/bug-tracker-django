import environ

env = environ.Env()

SUPERUSER = 'Superuser'
MANAGER = 'Manager'
DEVELOPER = 'Developer'
REQUESTER = 'Requester'
ALL_GROUPS = [MANAGER, DEVELOPER, REQUESTER]
ADMINS = [SUPERUSER, MANAGER]

TIMESTAMP_EXCLUDE = ['creator', 'updater', 'created_at', 'updated_at']

PAG_BY = 10

SUPERUSER_USERNAME = str(env('SUPERUSER_USERNAME'))

MONTH = 2628288
YEAR = 2023  # todo make this the current year
