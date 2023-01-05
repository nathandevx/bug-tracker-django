from django.views.generic import TemplateView, ListView

from bug_tracker.constants import ALL_GROUPS, PAG_BY
from tracker.mixins import GroupsRequiredMixin
from tracker.models import Ticket


class Dashboard(GroupsRequiredMixin, TemplateView):
	template_name = 'tracker/dashboard/dashboard.html'
	groups = ALL_GROUPS


class AllTicketListView(GroupsRequiredMixin, ListView):
	model = Ticket
	template_name = 'tracker/dashboard/all_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.all()


class ResolvedTicketListView(GroupsRequiredMixin, ListView):
	model = Ticket
	template_name = 'tracker/dashboard/resolved_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.filter(status=Ticket.RESOLVED)


class InProgressTicketListView(GroupsRequiredMixin, ListView):
	model = Ticket
	template_name = 'tracker/dashboard/in_progress_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.filter(status=Ticket.IN_PROGRESS)


class HighPriorityTicketListView(GroupsRequiredMixin, ListView):
	model = Ticket
	template_name = 'tracker/dashboard/in_progress_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.filter(priority=Ticket.HIGH)

