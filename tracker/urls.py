from django.urls import path
from tracker.views import general

app_name = 'tracker'
urlpatterns = [
    path("dashboard/", general.Dashboard.as_view(), name="dashboard"),
]
