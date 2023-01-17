from django import forms
from tracker.models import Tracker, Ticket, TicketComment

TIMESTAMP_EXCLUDE = ['creator', 'updater', 'created_at', 'updated_at']


class TrackerForm(forms.ModelForm):
	class Meta:
		model = Tracker
		exclude = TIMESTAMP_EXCLUDE


class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		_exclude = ['resolution', 'assignees', 'tracker']
		exclude = TIMESTAMP_EXCLUDE + _exclude


class TicketCommentForm(forms.ModelForm):
	class Meta:
		model = TicketComment
		_exclude = ['ticket']
		exclude = TIMESTAMP_EXCLUDE + _exclude
