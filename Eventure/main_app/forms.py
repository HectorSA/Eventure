from django.forms import formset_factory
from django import forms
from .models import *

class EmailInviteeForm(forms.ModelForm):
	class Meta:
		model = Attendee
		fields = ('email', )

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name','amount',)

class CreateEventForm(forms.ModelForm):
	class Meta:
		model = EventInfo
		fields = ('id','host','type','name','location','date','time','description','eventPhoto',)