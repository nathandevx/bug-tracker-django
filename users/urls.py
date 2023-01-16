from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
	path('signup/', views.SignUpView.as_view(), name='register'),
	path("login/", views.LoginView.as_view(), name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("update/<int:pk>/", views.UpdateProfileView.as_view(), name="update"),
	path("update-password/<int:pk>/", views.update_password, name="update-password"),
	path("detail/<int:pk>/", views.ProfileView.as_view(), name="detail"),
]
