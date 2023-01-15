from django import forms
from django.contrib.auth import get_user_model


class UserBaseForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'password']
		widgets = {
			'password': forms.PasswordInput()
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

