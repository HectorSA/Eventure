from django.forms import formset_factory
from django import forms
from .models import *

class EmailInviteeForm(forms.ModelForm):
	class Meta:
		model = Attendee
		fields = ('email',)
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class RegisterForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('firstName', 'lastName', 'city', 'state', 'zip',)

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name','amount',)

class CreateEventForm(forms.ModelForm):
	class Meta:
		model = EventInfo
		fields = ('id','host','type','name','location','date','time','description','eventPhoto',)