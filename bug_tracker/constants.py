import environ

env = environ.Env()

# Groups
SUPERUSER = 'Superuser'
MANAGER = 'Manager'
DEVELOPER = 'Developer'
SUBMITTER = 'Submitter'
DEMO = 'Demo'  # for demo users
ALL_GROUPS = [SUPERUSER, MANAGER, DEVELOPER, SUBMITTER, DEMO]
ADMINS = [SUPERUSER, MANAGER]

# Users
SUPERUSER_USERNAME = str(env('SUPERUSER_USERNAME'))
# Demo users
MANAGER_CREDENTIALS = str(env('MANAGER_CREDENTIALS'))
DEVELOPER_CREDENTIALS = str(env('DEVELOPER_CREDENTIALS'))
SUBMITTER_CREDENTIALS = str(env('SUBMITTER_CREDENTIALS'))

# View constants
PAG_BY = 10


MONTH = 2628288
YEAR = 2023  # todo make this the current year
