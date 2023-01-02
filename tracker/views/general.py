from django.views.generic import TemplateView
from bug_tracker.constants import ALL_GROUPS
from tracker.mixins import GroupsRequiredMixin


class Dashboard(GroupsRequiredMixin, TemplateView):
	template_name = 'tracker/general/dashboard.html'
	groups = ALL_GROUPS

