import datetime
import random
from django.utils import timezone


def get_random_date(seconds: int = 15000000):
	"""
	15,000,000 seconds is about 6 months
	:return: A random date between now and the given amount of seconds
	"""
	return timezone.now() + datetime.timedelta(seconds=random.randint(0, 86400))


def is_member(user, group: str):
	return user.groups.filter(name=group).exists()
