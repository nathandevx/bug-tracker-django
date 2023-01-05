from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import uuid

from tracker.models import Tracker, Ticket, TicketComment
from bug_tracker.utils import get_random_date
from bug_tracker.constants import SUPERUSER_USERNAME


class Command(BaseCommand):
	"""
	Fills database with dummy data.
	"""
	help = 'Fills database with dummy data.'
	User = get_user_model()

	def generate_users(self):
		# Generate 5 users who are in the manager group
		for i in range(5):
			user = self.User.objects.create(username=f'manager{i+1}', password=str(uuid.uuid4()), first_name=f'first{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Manager')
			group.user_set.add(user)
			user.save()
		for i in range(10):
			user = self.User.objects.create(username=f'developer{i+1}', password=str(uuid.uuid4()), first_name=f'firstd{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Developer')
			group.user_set.add(user)
			user.save()

		for i in range(20):
			user = self.User.objects.create(username=f'submitter{i+1}', password=str(uuid.uuid4()), first_name=f'firsts{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Submitter')
			group.user_set.add(user)
			user.save()
		self.stdout.write('generate_users finished')

	def generate_trackers(self):
		for i in range(10):
			user = self.User.objects.filter(groups__name='Manager').exclude(username=SUPERUSER_USERNAME).order_by('?').first()
			# user = self.User.objects.exclude(username=SUPERUSER_USERNAME).random()
			print(f'Random user: {user}')
			Tracker.objects.create(title=f'tracker{i+1}', description='desc', creator=user, updater=user, created_at=get_random_date(), updated_at=timezone.now())

	def handle(self, *args, **kwargs):
		call_command('delete_data')

		# Generate 100 tickets with random status, assignee, etc
			# Then generate 1-10 TicketComments per ticket
		self.generate_users()
		self.stdout.write('generate_users finished')
		self.generate_trackers()
		self.stdout.write('generate_trackers finished')
		self.stdout.write('make_data finished')


