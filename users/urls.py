from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
	path('signup/', views.SignUpView.as_view(), name='register'),
	path("login/", views.LoginView.as_view(), name="login"),
	path("logout/", views.logout_view, name="logout"),

	path("update/<int:pk>/", views.UpdateProfileView.as_view(), name="update"),
	path("update-password/<int:pk>/", views.UpdatePasswordView.as_view(), name="update-password"),

	path("detail/<int:pk>/", views.ProfileView.as_view(), name="detail"),

	path("demo-manager/", views.demo_manager, name="demo-manager"),
	path("demo-developer/", views.demo_developer, name="demo-developer"),
	path("demo-submitter/", views.demo_submitter, name="demo-submitter"),

]
