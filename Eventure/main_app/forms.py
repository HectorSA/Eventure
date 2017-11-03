from django.forms import formset_factory
from django import forms
from .models import *
from .models import UserProfile
from django.forms import ModelForm
from django.forms import ValidationError

EVENT_TYPE_CHOICES = (
    (True, 'Private'),
    (False, 'Public')
)

			    
class EmailInviteeForm(forms.Form):
	email = forms.EmailField(max_length=256,
	                         widget=forms.TextInput(attrs={'placeholder': ' abc@xyz.com'},),
	                         )

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class RegisterForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('firstName', 'lastName', 'city', 'state', 'zip',)
		
class ItemForm(forms.Form):
	itemName = forms.CharField(max_length=255, label = 'Item',
	                         widget=forms.TextInput(attrs={'placeholder': ' Pizza'}))
	amount = forms.IntegerField()

class itemMForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name','amount',)

class takeItemForm(forms.ModelForm):
	class Meta:
		model = TakenItem
		fields = ('itemBeingBroughtID', 'attendeeID','itemLinkID','eventID','quantity','comment',)
		
class CreateEventForm(forms.ModelForm):

	type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, label="Event Type",
	                              initial=True, widget=forms.Select(), required=True)

	class Meta:

		model = EventInfo
		fields = ('name','location','date','time','description','type','eventCategory','eventPhoto',)
		labels = {
			'name' : 'Event Name',
			'eventCategory': 'Event Category'
		}

class userLoginForm(forms.Form):
	username = forms.CharField(label='User Name', max_length=32)
	password = forms.CharField(label='Password', widget=forms.PasswordInput())

class LandingViewForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('user','id','firstName','lastName','city','state','zip',)