import environ

env = environ.Env()

MANAGER = 'Manager'
DEVELOPER = 'Developer'
REQUESTER = 'Requester'
ALL_GROUPS = [MANAGER, DEVELOPER, REQUESTER]

TIMESTAMP_EXCLUDE = ['creator', 'updater', 'created_at', 'updated_at']

PAG_BY = 10

SUPERUSER_USERNAME = str(env('SUPERUSER_USERNAME'))
