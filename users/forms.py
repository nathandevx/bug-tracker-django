from django import forms
from django.contrib.auth import get_user_model, authenticate


class UserBaseForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number']
		# todo validate phone number input

	def save(self, commit=True):
		user = super().save(commit=False)
		# Set password
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
		# todo validate phone number input

class UpdateProfileForm(UserBaseForm):
	pass


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=128)

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if not user:
			self.add_error(None, "Incorrect username or password")
