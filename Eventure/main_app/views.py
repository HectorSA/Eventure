from django.shortcuts import render
import random, string
from .forms import *
from django.forms import formset_factory

WEBSITENAME = 'Eventure'
# Create your views here.

# Used to display an event from a URL given to anon users from an email
def displayEvent(request, groupID, userID):
	print("groupID:%s -- userID:%s -- website %s" % (groupID, userID, WEBSITENAME))

def index(request):
    return render(request, 'index.html', {})

def createEvent(request):

	EmailFormSet = formset_factory(EmailInviteeForm)
	ItemFormSet = formset_factory(ItemForm)
	EventForm = CreateEventForm()
	
	if request.method == 'POST':
		inviteToEventFormset = EmailFormSet(request.POST, request.FILES)
		if inviteToEventFormset.is_valid():
			pass
		
		itemCreationFormset = ItemFormSet(request.POST, request.FILES)
		if itemCreationFormset.is_valid():
			pass
	else:
		inviteToEventFormset = EmailFormSet()
		itemCreationFormset = ItemFormSet()
	
	mapping = {
		'eventForm' : EventForm,
		'itemCreationFormset': itemCreationFormset,
		'inviteToEventFormset': inviteToEventFormset,
	}
	
	return render(request, 'createEvent.html', mapping)


################# Functions used by views #################
# Will return a string of specified length of alphanumeric characters
def createAlphanumericSequence(sequenceLength):
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits) \
	                        for digits in range(sequenceLength))
	
def createURL():
	eventID = createAlphanumericSequence(10)
	userID = createAlphanumericSequence(6)
	
	print(eventID + userID)
	
############################################################