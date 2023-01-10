from django.contrib.auth.models import AbstractUser
from bug_tracker.constants import YEAR


class User(AbstractUser):
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
