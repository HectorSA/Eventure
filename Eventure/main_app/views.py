from django.shortcuts import render
import random, string

WEBSITENAME = 'Eventure'
# Create your views here.

# Used to display an event from a URL given to anon users from an email
def displayEvent(request, groupID, userID):
	print("groupID:%s -- userID:%s -- website %s" % (groupID, userID, WEBSITENAME))
	return render(request, 'DisplayEvent.html')

# Will return a string of specified length of alphanumeric characters
def createAlphanumericSequence(sequenceLength):
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits) \
	                        for digits in range(sequenceLength))
	
# 
def createURL():
	groupID = createAlphanumericSequence(10)
	userID = createAlphanumericSequence(6)
	
	print(groupID + userID)