from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DetailView
from django.shortcuts import reverse, redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseServerError

from tracker.mixins import GroupsRequiredMixin
from .forms import LoginForm, SignupForm, UpdateProfileForm
from bug_tracker.constants import SUPERUSER, ALL_GROUPS, MANAGER_CREDENTIALS, DEVELOPER_CREDENTIALS, SUBMITTER_CREDENTIALS
from bug_tracker.utils import is_member


# todo password reset?
# todo - demo users - what if they're logged in, should they not be given "delete" permissions?
# todo - shouldn't be able to update anything about demo users
class SignUpView(UserPassesTestMixin, CreateView):
	model = get_user_model()
	form_class = SignupForm
	template_name = 'users/signup.html'

	def form_valid(self, form):
		user = form.save(commit=False)
		user.set_password(form.cleaned_data['password'])
		user.save()
		group = Group.objects.get(name='Submitter')
		group.user_set.add(user)
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user is not None:
			login(self.request, user)
			return super().form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('tracker:dashboard')

	def test_func(self):
		# don't allow logged in users to access page
		return not self.request.user.is_authenticated


class LoginView(UserPassesTestMixin, FormView):
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
		return reverse('tracker:dashboard')

	def test_func(self):
		# don't allow logged in users to access page
		return not self.request.user.is_authenticated


class UpdateProfileView(UserPassesTestMixin, UpdateView):
	model = get_user_model()
	form_class = UpdateProfileForm
	template_name = 'users/update.html'
	context_object_name = 'user_obj'  # needed or will conflict with default 'user' template variable

	def get_success_url(self):
		return self.object.get_absolute_url()

	def test_func(self):
		is_creator = self.get_object() == self.request.user
		is_admin = is_member(self.request.user, SUPERUSER)
		return is_creator or is_admin


class UpdatePasswordView(UserPassesTestMixin, PasswordChangeView):
	form_class = PasswordChangeForm
	template_name = 'users/update_password.html'

	def form_valid(self, form):
		update_session_auth_hash(self.request, self.request.user)  # lets the user stay logged in
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('users:detail', kwargs={'pk': self.kwargs['pk']})

	def test_func(self):
		is_creator = self.kwargs['pk'] == self.request.user.pk
		is_admin = is_member(self.request.user, SUPERUSER)
		return is_creator or is_admin


class ProfileView(GroupsRequiredMixin, DetailView):
	model = get_user_model()
	template_name = 'users/detail.html'
	groups = ALL_GROUPS
	context_object_name = 'user_obj'  # needed or will conflict with default 'user' template variable

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# todo what if they are a developer or manager? what should they see
		context['access'] = (self.object == self.request.user) or (is_member(self.request.user, SUPERUSER))
		return context


def logout_view(request):
	logout(request)
	return redirect(reverse('home:home'))


def demo_manager(request):
	username, password, group, first_name, last_name, email, phone_number = MANAGER_CREDENTIALS.split(',')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect(reverse('tracker:dashboard'))
	else:
		return HttpResponseServerError()


def demo_developer(request):
	username, password, group, first_name, last_name, email, phone_number = DEVELOPER_CREDENTIALS.split(',')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect(reverse('tracker:dashboard'))
	else:
		return HttpResponseServerError()


def demo_submitter(request):
	username, password, group, first_name, last_name, email, phone_number = SUBMITTER_CREDENTIALS.split(',')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect(reverse('tracker:dashboard'))
	else:
		return HttpResponseServerError()
