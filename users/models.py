from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Case, When, IntegerField

from bug_tracker.constants import YEAR, SUPERUSER_USERNAME


class User(AbstractUser):
	phone_number = models.CharField(max_length=20, default='000-000-0000')

	@classmethod
	def get_year_months_total_users(cls, year: int = YEAR):
		"""
		:param year: The year.
		:return: A tuple of 2 lists. The first being a list of the months. The other being a list of the total
		number of users created in that month.
		"""
		months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		months_ticket_totals = []
		for i, month in enumerate(months):
			total = cls.objects.filter(date_joined__year=year, date_joined__month=i + 1).count()
			months_ticket_totals.append(total)
		return months, months_ticket_totals

	@classmethod
	def get_all_users_not_superuser(cls, sort: str = 'role', desc_asc: str = 'desc'):
		"""
		Gets all users but the superuser in random order.
		It's in random order so you can sort them (like in the users table)
		:return: queryset of users
		"""
		ordering = '-'
		if desc_asc == 'asc':  # ASC
			ordering = ''

		if sort == 'username':
			return cls.objects.exclude(username=SUPERUSER_USERNAME).order_by(f'{ordering}username')
		elif sort == 'date_joined':
			return cls.objects.exclude(username=SUPERUSER_USERNAME).order_by(f'{ordering}date_joined')
		# default sort by role
		# todo what if they are not in a group
		return cls.objects.exclude(username=SUPERUSER_USERNAME).annotate(group_order=Case(
			When(groups__name='Manager', then=0),
			When(groups__name='Developer', then=1),
			When(groups__name='Submitter', then=2),
			output_field=IntegerField()
		)).order_by(f'{ordering}group_order')

