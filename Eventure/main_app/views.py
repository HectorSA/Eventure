from django.shortcuts import render
import random, string

# Create your views here.

# Will return a group id, a string of 10 digits
def createGroupID():
	digitSequence = ''.join(random.choice(string.digits) for digits in range(10))
	print(digitSequence)

#
def createUserID():
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits) \
	                        for digits in range(16))
	print(alphaNumericSequence)
	
def createURL():
	groupID = createGroupID()
	userID = createUserID()
	
	print(groupID + userID)