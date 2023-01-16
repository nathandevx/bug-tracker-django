from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group

from tracker.mixins import GroupsRequiredMixin
from tracker.models import Ticket
from .forms import UserBaseForm, LoginForm
from bug_tracker.constants import SUPERUSER, ALL_GROUPS
from bug_tracker.utils import is_member

# todo change the model name of all user views


class SignUpView(CreateView):
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
		print(user)
		print(self.request)
		if user is not None:
			login(self.request, user)
			return super().form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('tracker:dashboard')


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
		return reverse('tracker:dashboard')


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


class ProfileView(GroupsRequiredMixin, DetailView):
	model = get_user_model()
	template_name = 'users/detail.html'
	groups = ALL_GROUPS
	context_object_name = 'user_obj'  # needed or will conflict with default 'user' template variable

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# todo what if they are a developer or manager? what should they see
		# context['tickets'] = Ticket.objects.filter(creator=self.request.user)
		context['access'] = (self.object == self.request.user) or (is_member(self.request.user, SUPERUSER))
		return context


def logout_view(request):
	logout(request)
	return redirect(reverse('home:home'))

