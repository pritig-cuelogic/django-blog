from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Category

class RegisterForm(forms.Form):
	username = forms.CharField(label="Username", max_length=30)
	email = forms.EmailField(label="Email", max_length=254)
	password1 = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm Password", max_length=30, widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords and confirm password didn't match.")
		return self.cleaned_data

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="MyUsername", max_length=30)
	password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)

class CreatePostForm(forms.Form):
	title = forms.CharField(max_length=200)
	content = forms.CharField(widget=forms.Textarea)
	Category = forms.ModelChoiceField(
		queryset=Category.objects.all().order_by('id'),
		 empty_label="select category",to_field_name="id")
