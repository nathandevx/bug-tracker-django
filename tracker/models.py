from django.db import models
from django.conf import settings


class TimestampCreatorMixin(models.Model):
	creator = models.ForeignKey(verbose_name="Creator", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_creator')
	updater = models.ForeignKey(verbose_name="Updater", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_updater')
	created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)

	class Meta:
		abstract = True
		verbose_name = "TimestampCreatorMixin"
		verbose_name_plural = "TimestampCreatorMixin"


class Tracker(TimestampCreatorMixin):
	title = models.CharField(verbose_name="Title", default='', max_length=20)
	description = models.TextField(verbose_name="Description", default='', max_length=500)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Tracker"
		verbose_name_plural = "Trackers"


class Ticket(TimestampCreatorMixin):
	# TYPE CHOICES
	FEATURE = 'FEATURE'
	BUG = 'BUG'
	UI = 'UI'
	TYPE_CHOICES = [
		(BUG, 'Bug'),
		(UI, 'User-Interface'),
		(FEATURE, 'Feature'),
	]  # (stored, displayed)

	# status CHOICES
	OPEN = 'OPEN'
	CLOSED = 'CLOSED'
	IN_PROGRESS = 'IN PROGRESS'
	RESOLVED = 'RESOLVED'
	STATUS_CHOICES = [
		(OPEN, 'Open'),
		(IN_PROGRESS, 'In progress'),
		(RESOLVED, 'Resolved'),
		(CLOSED, 'Closed'),
	]

	# PRIORITY CHOICES
	HIGH = 'HIGH'
	NORMAL = 'NORMAL'
	LOW = 'LOW'
	PRIORITY_CHOICES = [
		(HIGH, 'High'),
		(NORMAL, 'Normal'),
		(LOW, 'Low'),
	]
	title = models.CharField(verbose_name="Title", default='', max_length=20)
	description = models.TextField(verbose_name="Description", default='', max_length=500)
	resolution = models.TextField(verbose_name="Resolution", default='', max_length=500)
	type = models.CharField(verbose_name="Type", default=BUG, max_length=11, choices=TYPE_CHOICES)
	status = models.CharField(verbose_name="Status", default=OPEN, max_length=11, choices=STATUS_CHOICES)
	priority = models.CharField(verbose_name="Priority", default=NORMAL, max_length=8, choices=PRIORITY_CHOICES)
	assignees = models.ManyToManyField(verbose_name="Assignees", blank=True, to=settings.AUTH_USER_MODEL, related_name='assignees')
	tracker = models.ForeignKey(verbose_name="Tracker", to=Tracker, on_delete=models.CASCADE)
	# todo add attachment file field

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Ticket"
		verbose_name_plural = "Tickets"


class TicketComment(TimestampCreatorMixin):
	title = models.CharField(verbose_name="Title", default='', max_length=20)
	description = models.TextField(verbose_name="Comment", default='', max_length=500)
	ticket = models.ForeignKey(verbose_name="Ticket", to=Ticket, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Ticket comment"
		verbose_name_plural = "Ticket comments"