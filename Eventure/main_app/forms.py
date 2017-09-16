from django.forms import formset_factory
from django import forms
from .models import *


class InviteeForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('itemID','eventID','name','amount','isTaken',)
