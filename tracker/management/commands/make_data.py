from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from random import randint, choice
import uuid

from tracker.models import Tracker, Ticket, TicketComment
from bug_tracker.utils import get_random_date, get_random_date_after_a_date, get_random_phone_number
from bug_tracker.constants import SUPERUSER_USERNAME, MONTH


class Command(BaseCommand):
	"""
	Fills database with dummy data.
	"""
	help = 'Fills database with dummy data.'
	User = get_user_model()

	@staticmethod
	def delete_data():
		Tracker.objects.all().delete()
		Ticket.objects.all().delete()
		TicketComment.objects.all().delete()
		get_user_model().objects.exclude(username='code').delete()

	def generate_users(self):
		"""
		Generates Users and assigns them to Managers, Developers, or Submitters
		"""
		for i in range(3):
			user = self.User.objects.create(username=f'manager{i+1}', email=f'manager{i+1}@example.com', first_name=f'first{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Manager')
			group.user_set.add(user)
			user.date_joined = get_random_date()
			user.phone_number = get_random_phone_number()
			user.set_password(str(uuid.uuid4()))
			user.save()
		for i in range(5):
			user = self.User.objects.create(username=f'developer{i+1}', email=f'developer{i+1}@example.com', first_name=f'firstd{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Developer')
			group.user_set.add(user)
			user.date_joined = get_random_date()
			user.phone_number = get_random_phone_number()
			user.set_password(str(uuid.uuid4()))
			user.save()
		for i in range(20):
			user = self.User.objects.create(username=f'submitter{i+1}', email=f'submitter{i+1}@example.com', first_name=f'firsts{i+1}', last_name=f'last{i+1}')
			group = Group.objects.get(name='Submitter')
			group.user_set.add(user)
			user.date_joined = get_random_date()
			user.phone_number = get_random_phone_number()
			user.set_password(str(uuid.uuid4()))
			user.save()

	def generate_trackers(self):
		"""
		Generates Trackers for Users who're Managers
		:return:
		"""
		for i in range(10):
			# Gets user in group "Manager", excluding the superuser, in random order, and gets the first result
			user = self.User.objects.filter(groups__name='Manager').exclude(username=SUPERUSER_USERNAME).order_by('?').first()
			tracker = Tracker.objects.create(title=f'tracker{i+1}', description='desc', creator=user, updater=user)
			tracker.created_at = get_random_date()  # todo what if a Ticket/TicketComment 'created_at' is before the tracker's 'created_at'
			tracker.updated_at = get_random_date_after_a_date(tracker.created_at, MONTH)
			tracker.save()

	def generate_tickets(self):
		"""
		Generates Tickets and TicketComments
		"""
		for i in range(30):
			# Get random choices
			typee = Ticket.TYPE_CHOICES[randint(0, 2)][0]
			status = Ticket.STATUS_CHOICES[randint(0, 3)][0]
			priority = Ticket.PRIORITY_CHOICES[randint(0, 2)][0]

			# Get 0-3 random developers
			developers = self.User.objects.filter(groups__name='Developer').exclude(username=SUPERUSER_USERNAME).order_by('?')[:randint(0, 3)]
			# Get a random submitter
			submitter = self.User.objects.filter(groups__name='Submitter').exclude(username=SUPERUSER_USERNAME).order_by('?').first()
			# Get a random tracker
			tracker = Tracker.objects.order_by('?').first()

			# Create the ticket
			ticket = Ticket.objects.create(title=f'ticket{i+1}', description='desc',
								   creator=submitter, updater=submitter,
								   resolution='resolution', type=typee, status=status, priority=priority, tracker= tracker)
			# Update the dates
			ticket.created_at = get_random_date()  # need to do this because 'created_at' automatically assigns a value
			ticket.updated_at = get_random_date_after_a_date(ticket.created_at, MONTH*3)

			# Assign developers to tickets
			for dev in developers:
				ticket.assignees.add(dev)
			ticket.save()

			# Generate TicketComment's (the creator is the submitter)
			for j in range(randint(0, 5)):
				num = randint(0, 1)
				comment = TicketComment.objects.create(title=f'comment{j+1}', description=f'desc{j+1}', ticket=ticket, creator=submitter, updater=submitter)
				comment.created_at = get_random_date()
				comment.updated_at = get_random_date_after_a_date(comment.created_at, MONTH // 4)
				if num == 0 and developers:  # make a developer assigned to the ticket the commenter (if one exists)
					comment.creator = choice(developers)
					comment.updater = choice(developers)
					comment.save()

	def handle(self, *args, **kwargs):
		self.delete_data()
		self.stdout.write('delete_data finished')

		self.generate_users()
		self.stdout.write('generate_users finished')

		self.generate_trackers()
		self.stdout.write('generate_trackers finished')

		self.generate_tickets()
		self.stdout.write('generate_tickets finished')

		self.stdout.write('make_data finished')
