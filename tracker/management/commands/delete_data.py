from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from tracker.models import Tracker, Ticket, TicketComment


class Command(BaseCommand):
	help = 'Deletes tracker, ticket, ticketcomment, user (not superuser) data'

	def handle(self, *args, **kwargs):
		Tracker.objects.all().delete()
		Ticket.objects.all().delete()
		TicketComment.objects.all().delete()
		get_user_model().objects.exclude(username='code').delete()
		self.stdout.write('delete_data finished')
