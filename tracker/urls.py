from django.urls import path
from tracker.views import general

app_name = 'tracker'
urlpatterns = [
    path("dashboard/", general.Dashboard.as_view(), name='dashboard'),
    path("open-tickets/", general.OpenTicketListView.as_view(), name='open-tickets'),
    path("resolved-tickets/", general.ResolvedTicketListView.as_view(), name='resolved-tickets'),
    path("in-progress-tickets/", general.InProgressTicketListView.as_view(), name='in-progress-tickets'),
    path("high-priority-tickets/", general.HighPriorityTicketListView.as_view(), name='high-priority-tickets'),
]
