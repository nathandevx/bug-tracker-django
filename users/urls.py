from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
	path('register/', views.SignUpView.as_view(), name='register'),
	path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("update-profile/", views.UpdateProfileView.as_view(), name="update-profile"),  # todo add extra fields like phone, email, etc
]
