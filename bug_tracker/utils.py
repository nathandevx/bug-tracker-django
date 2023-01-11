import datetime
import random
from django.utils import timezone


def get_random_phone_number():
	number = str(random.randint(1000000000, 9999999999))
	formatted_number = "{}-{}-{}".format(number[:3], number[3:6], number[6:])
	return formatted_number


def get_random_date(seconds: int = 31536000):
	"""
	2,628,288 = 30 days
	31,536,000 = 365 days
	:return: A random date between now and the given amount of seconds
	"""
	return timezone.now() + datetime.timedelta(seconds=random.randint(0, seconds))


def get_random_date_after_a_date(date, seconds: int = 2628288):
	"""
	Gets a random date after a given date.
	:param date: the date to add onto
	:param seconds: how long after 'date' a random date should be generated
	:return: a date.
	"""
	return date + datetime.timedelta(seconds=random.randint(0, seconds))


def is_member(user, group: str):
	return user.groups.filter(name=group).exists()
