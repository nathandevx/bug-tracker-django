from django import forms
from django.contrib.auth import get_user_model


class UserModelForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'password']
		widgets = {
			'password': forms.PasswordInput()
		}
