from django import forms
from tracker.models import Tracker, Ticket, TicketComment
from bug_tracker.constants import TIMESTAMP_EXCLUDE


class TrackerModelForm(forms.ModelForm):
	class Meta:
		model = Tracker
		exclude = TIMESTAMP_EXCLUDE


class TicketModelForm(forms.ModelForm):
	class Meta:
		model = Ticket
		_exclude = ['resolution', 'assignees', 'tracker']
		exclude = TIMESTAMP_EXCLUDE + _exclude


class TicketCommentModelForm(forms.ModelForm):
	class Meta:
		model = TicketComment
		_exclude = ['ticket']
		exclude = TIMESTAMP_EXCLUDE + _exclude