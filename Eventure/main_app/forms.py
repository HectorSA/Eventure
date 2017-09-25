from django.forms import formset_factory
from django import forms
from .models import *
from django.forms import ModelForm


class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.help_text
                })
			    
class EmailInviteeForm(forms.Form):
	email = forms.EmailField(max_length=256,
	                         widget=forms.TextInput(attrs={'placeholder': ' abc@xyz.com'}))

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class RegisterForm(BaseModelForm):
	class Meta:
		model = UserProfile
		fields = ('firstName', 'lastName', 'profilePhoto','city', 'state', 'zip',)
		help_texts = {
			'firstName': 'John',
			'lastName' : 'Doe',
			'city' : 'San Antonio',
			'zip': '78324',
		}
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