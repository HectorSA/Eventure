from django.forms import formset_factory
from django import forms
from .models import *

class EmailInviteeForm(forms.Form):
	email = forms.EmailField(max_length=256,
	                         widget=forms.TextInput(attrs={'placeholder': ' abc@xyz.com'}))

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class RegisterForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('firstName', 'lastName', 'profilePhoto','city', 'state', 'zip',)

class ItemForm(forms.Form):
	itemName = forms.CharField(max_length=255, label = 'Item',
	                         widget=forms.TextInput(attrs={'placeholder': ' Pizza'}))
	amount = forms.IntegerField()


class CreateEventForm(forms.ModelForm):
	class Meta:
		model = EventInfo
		fields = ('name','location','date','time','description','eventPhoto',)

class userLoginForm(forms.Form):
	userName = forms.CharField(label='userName', max_length=32)
	password = forms.CharField(label='password', widget=forms.PasswordInput())