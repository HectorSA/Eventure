from django.shortcuts import render
import random, string
from .forms import *
from django.forms import formset_factory

WEBSITENAME = 'Eventure'
# Create your views here.

# Used to display an event from a URL given to anon users from an email
def displayEvent(request, groupID, userID):
	print("groupID:%s -- userID:%s -- website %s" % (groupID, userID, WEBSITENAME))



def createEvent(request):
	
	## Select what item
	
	## Create a formset from the ItemForm
	ItemFormSet = formset_factory(ItemForm)
	if request.method == 'POST':
		itemCreationFormset = ItemFormSet(request.POST, request.FILES)
		if itemCreationFormset.is_valid():
			# do something with the formset.cleaned_data
			pass
	else:
		itemCreationFormset = ItemFormSet()
	
	return render(request, 'createEvent.html', {'itemCreationFormset': itemCreationFormset})


################# Functions used by views #################
# Will return a string of specified length of alphanumeric characters
def createAlphanumericSequence(sequenceLength):
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits) \
	                        for digits in range(sequenceLength))
	
def createURL():
	groupID = createAlphanumericSequence(10)
	userID = createAlphanumericSequence(6)
	
	print(groupID + userID)
	
############################################################