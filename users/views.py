from django.views.generic import TemplateView, CreateView, FormView
from django.shortcuts import reverse, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from .model_forms import UserModelForm
from .forms import LoginForm


class SignUpView(CreateView):
	model = get_user_model()
	form_class = UserModelForm
	template_name = 'users/signup.html'

	def form_valid(self, form):
		# low check if username exists (built in)
		user = form.save(commit=False)
		user.set_password(form.cleaned_data['password'])
		user.save()
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		login(self.request, user)
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('home:home')


class LoginView(FormView):
	form_class = LoginForm
	template_name = 'users/login.html'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(self.request, username=username, password=password)
		if user is not None:
			login(self.request, user)
			return super().form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('home:home')


def logout_view(request):
	logout(request)
	return redirect(reverse('home:home'))

