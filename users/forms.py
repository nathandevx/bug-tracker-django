from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(max_length=500)
	password = forms.CharField(max_length=500, widget=forms.PasswordInput)
