from django import forms
from django.contrib.auth import get_user_model


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


class UpdateProfileForm(UserBaseForm):
	pass


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=128, widget=forms.PasswordInput)
