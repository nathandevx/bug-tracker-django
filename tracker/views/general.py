from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model

from bug_tracker.constants import ALL_GROUPS, PAG_BY, ADMINS, YEAR
from tracker.mixins import GroupsRequiredMixin
from tracker.models import Ticket


class Dashboard(GroupsRequiredMixin, TemplateView):
	template_name = 'tracker/dashboard/dashboard.html'
	groups = ALL_GROUPS

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		sort = self.request.GET.get('sort')
		order = self.request.GET.get('order', 'asc')

		# Ticket data
		result = Ticket.get_year_months_total_tickets()
		context['ticket_months'] = result[0]
		context['ticket_data'] = result[1]

		# User data
		result = get_user_model().get_year_months_total_users()
		context['user_months'] = result[0]
		context['user_data'] = result[1]
		context['users'] = get_user_model().get_all_users_not_superuser(sort, order)

		# More
		context['access'] = self.request.user.groups.filter(name__in=ADMINS).exists()
		context['order'] = order
		context['year'] = YEAR
		return context


class OpenTicketListView(GroupsRequiredMixin, ListView):
	model = Ticket
	template_name = 'tracker/dashboard/open_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.filter(status=Ticket.OPEN)


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
	template_name = 'tracker/dashboard/high_priority_tickets.html'
	groups = ALL_GROUPS
	paginate_by = PAG_BY
	queryset = Ticket.objects.filter(priority=Ticket.HIGH)

