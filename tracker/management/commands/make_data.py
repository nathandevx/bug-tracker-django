from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import uuid
from random import randint

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
		"""
		Generates Users and assigns them to Managers, Developers, or Submitters
		"""
		for i in range(3):
			user = self.User.objects.create(username=f'manager{i+1}', password=str(uuid.uuid4()), first_name=f'first{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Manager')
			group.user_set.add(user)
			user.save()
		for i in range(5):
			user = self.User.objects.create(username=f'developer{i+1}', password=str(uuid.uuid4()), first_name=f'firstd{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Developer')
			group.user_set.add(user)
			user.save()
		for i in range(20):
			user = self.User.objects.create(username=f'submitter{i+1}', password=str(uuid.uuid4()), first_name=f'firsts{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Submitter')
			group.user_set.add(user)
			user.save()

	def generate_trackers(self):
		"""
		Generates Trackers for Users who're Managers
		:return:
		"""
		for i in range(10):
			# Gets user in group "Manager", excluding the superuser, in random order, and gets the first result
			user = self.User.objects.filter(groups__name='Manager').exclude(username=SUPERUSER_USERNAME).order_by('?').first()
			Tracker.objects.create(title=f'tracker{i+1}', description='desc', creator=user, updater=user, created_at=get_random_date(), updated_at=timezone.now())

	def generate_tickets(self):
		"""
		Generates Tickets and TicketComments
		"""
		for i in range(30):
			typee = Ticket.TYPE_CHOICES[randint(0, 2)][0]
			status = Ticket.STATUS_CHOICES[randint(0, 3)][0]
			priority = Ticket.PRIORITY_CHOICES[randint(0, 2)][0]

			developers = self.User.objects.filter(groups__name='Developer').exclude(username=SUPERUSER_USERNAME).order_by('?')[:randint(0, 3)]
			submitter = self.User.objects.filter(groups__name='Submitter').exclude(username=SUPERUSER_USERNAME).order_by('?').first()
			tracker = Tracker.objects.order_by('?').first()

			ticket = Ticket.objects.create(title=f'ticket{i+1}', description='desc',
								   creator=submitter, updater=submitter, created_at=get_random_date(), updated_at=timezone.now(),
								   resolution='resolution', type=typee, status=status, priority=priority, tracker= tracker)
			# Assign developers to tickets
			for dev in developers:
				ticket.assignees.add(dev)
			ticket.save()

			# Generate TicketComment's (the creator is the submitter)
			for j in range(randint(0, 5)):
				# low the creator of a ticketcomment can also be a developer
				TicketComment.objects.create(title=f'comment{j+1}', description=f'desc{j+1}', ticket=ticket,
											 creator=submitter, updater=submitter, created_at=get_random_date(), updated_at=timezone.now())

	def handle(self, *args, **kwargs):
		call_command('delete_data')

		self.generate_users()
		self.stdout.write('generate_users finished')

		self.generate_trackers()
		self.stdout.write('generate_trackers finished')

		self.generate_tickets()
		self.stdout.write('generate_tickets finished')

		self.stdout.write('make_data finished')
