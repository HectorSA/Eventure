from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, render_to_response, redirect
import random, string
from .forms import *
from .forms import userLoginForm
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
WEBSITENAME = 'Eventure'
groupIDLength = 12
userIDLength = 8

# Create your views here.


def register(request):
	registered = False

	if request.method == 'POST':

		# Get info from "both" forms
		# It appears as one form to the user on the .html page
		user_form = UserForm(request.POST)
		user_profile_form = RegisterForm(request.POST)

		# Check to see both forms are valid
		if user_form.is_valid() and user_profile_form.is_valid():

			# Save User Form to Database
			user = user_form.save()

			# Hash the password
			user.set_password(user.password)

			# Update with Hashed password
			user.save()

			# Can't commit yet because we still need to manipulate
			profile = user_profile_form.save(commit=False)

			# Set One to One relationship between
			# UserForm and UserProfileInfoForm
			profile.user = user

			# Check if they provided a profile picture
			#if 'profilePhoto' in request.FILES:
			   # print('found it')
				# If yes, then grab it from the POST form reply
				#profile.profilePic = request.FILES['profilePhoto']

			# Now save model
			profile.save()

			# Registration Successful!
			registered = True

	else:
		# Was not an HTTP post so we just render the forms as blank.
		user_form = UserForm()
		user_profile_form = RegisterForm()

	# This is the render and context dictionary to feed
	# back to the registrationPage.html file page.
	mapping = {'user_form': user_form,
			   'user_profile_form': user_profile_form,
			   'registered': registered,
			   }

	return render(request, 'registrationPage.html', mapping)


# Used to display an event from a URL given to anon users from an email
def displayEvent(request, groupID, userID):
	event = findGroup(groupID)
	attendee = findAttendee(userID)
	if(request.method == 'GET'):
		if(event is not None):
			if(attendee is not None):
				rsvpStatus = getRSVPStatus(attendee.RSVPStatus)
				address = getParsedEventAddr(groupID)
				print(rsvpStatus)
				mapping = {
					'attendee':attendee,
					'event':event,
					'address':address,
					'rsvpStatus':rsvpStatus
				}
				return render(request, 'displayEvent.html', mapping)
			userID = findUser(request.user.id)
			if(userID.is_valid()):
				mapping = {
					'userID': userID,
					'event':event
				}
				return render(request, 'displayEvent.html',mapping)
	elif(request.method == 'POST'):
		if(attendee is not None):
			if '3' in request.POST:
				attendee
				print("is going")



def index(request):
	return render(request, 'index.html', {})

################## /createEvent ###################
def createEvent(request):
	EmailFormSet = formset_factory(EmailInviteeForm)
	ItemFormSet = formset_factory(ItemForm)
	
	## This is the eventID that will be assigned to email invitees
	eventID = 0
	newEvent = None
	if request.method == 'POST':
		eventForm = CreateEventForm(request.POST,request.FILES)
		
		if eventForm.is_valid():
			eventID = createAlphanumericSequence(groupIDLength)
			userID = findUser(request.user.id)
			eventType = eventForm.cleaned_data["type"]
			name = eventForm.cleaned_data["name"]
			location = eventForm.cleaned_data["location"]
			date = eventForm.cleaned_data["date"]
			time = eventForm.cleaned_data["time"]
			description = eventForm.cleaned_data["description"]
			
			newEvent = EventInfo(id = eventID, userProfile = userID, type = eventType, \
			                     name = name, location = location, date = date, \
			                     time = time, description = description, )
			if 'eventPhoto' in request.FILES:
				newEvent.eventPhoto = request.FILES['eventPhoto']
			newEvent.save()
			
			print('***********************************')
			print('{}{}'.format("Event: ", name))
			print('{}{}'.format("\tDUserID: ", request.user.id))
			print('{}{}'.format("\tUUserID: ", userID.id))
			print('{}{}'.format("\tType: ", eventType))
			print('{}{}'.format("\tLocation: ", location))
			print('{}{}'.format("\tDate: ", date))
			print('{}{}'.format("\tTime: ", time))
			print('{}{}'.format("\tDescription: ", description))
			print('{}{}'.format("\tEventID: ", eventID))
		
		inviteToEventFormset = EmailFormSet(request.POST, prefix='invitee')
		if inviteToEventFormset.is_valid():
			for invite in inviteToEventFormset:
				if invite.has_changed():
					emailUserID = createAlphanumericSequence(userIDLength)
					email = invite.cleaned_data["email"]
					print('{}{}{}{}'.format(email, " : http://127.0.0.1:8000/event/", newEvent.id, emailUserID))
					newEmailInvitee = Attendee(attendeeName = email, attendeeID = emailUserID, \
					                           eventID = newEvent, email = email, RSVPStatus = 1)
					newEmailInvitee.save()
		
		itemCreationFormset = ItemFormSet(request.POST, prefix='item')
		if itemCreationFormset.is_valid():
			for item in itemCreationFormset:
				if item.has_changed():
					itemName = item.cleaned_data["itemName"]
					itemAmount = item.cleaned_data["amount"]
					print('{}{}{}{}'.format("\tItem: ",itemName," x ",itemAmount))
					newItem = Item(eventID = newEvent, name = itemName, amount = itemAmount)
					newItem.save()

	else:
		eventForm = CreateEventForm()
		inviteToEventFormset = EmailFormSet(prefix='invitee')
		itemCreationFormset = ItemFormSet(prefix='item')

	mapping = {
		'eventForm': eventForm,
		'itemCreationFormset': itemCreationFormset,
		'inviteToEventFormset': inviteToEventFormset,
	}

	return render(request, 'createEvent.html', mapping)


################# Functions used by views #################
# Will return a string of specified length of alphanumeric characters
def createAlphanumericSequence(sequenceLength):
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits) \
								   for digits in range(sequenceLength))
	return alphaNumericSequence

###############getParsedEventAddress###################
def getParsedEventAddr(groupId):
	valueList = EventInfo.objects.filter(id = groupId).values_list('location',flat=True)
	newList = []
	newList.insert(0,"query=")
	newList.extend(valueList[0])
	i = 0
	for value in newList:
		if(value.isspace()):
			newList[i] = "+"
		i = i + 1
	address = ''.join(str(s) for s in newList)
	print(address)
	return address


####################get RSVP status ###################
def getRSVPStatus(rsvpNumber):
	NOTATTENDING = 1
	MAYBE = 2
	ATTENDING = 3

	RSVPSTATUS = {
		NOTATTENDING : "not attending",
		MAYBE: "undecided",
		ATTENDING: "attending"
	}
	return RSVPSTATUS[rsvpNumber]

################### findGorup ########################
def findGroup(groupID):
	eventInfo = EventInfo.objects.filter(id = groupID)
	return eventInfo


################### findUser ########################
# Pass a django UserID , get a Eventure User
def findUser(djangoUserID):
	eventureUser = UserProfile.objects.get(user_id=djangoUserID)
	return eventureUser

################### findAttendee ########################
# Pass a attendeeID get Attendee Object
def findAttendee(attendeeID):
	eventureAttendee = Attendee.objects.get(attendeeID=attendeeID)
	return eventureAttendee

################userLogin(request)#########################
def userLogin(request):
	if request.method == 'POST':
		loginForm = userLoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return render(request,'index.html')
				else:
					messages.info(request,'Sorry, this uses is not in our databse')
					return redirect('userLogin')
			else:
				messages.info(request, 'Sorry, wrong password/username.\n please try again\n')
				return redirect('userLogin')
	else:
		loginForm = userLoginForm()
		return render(request,'userLogin.html',{'loginForm':loginForm})

def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/')

def landingPageView(request):
	if request.method == 'GET':
		print("helllo")
		currentUser = findUser(request.user.id)
		userID = currentUser.id
		print('***********************************')
		print('{}{}'.format("\tDUserID: ", request.user.id))
		print('{}{}'.format("\tUUserID: ", currentUser.id))
		print('{}{}'.format("\tFirst Name: ", currentUser.firstName))
		print('{}{}'.format("\tLast Name: ", currentUser.lastName))
		print('{}{}'.format("\tCity: ", currentUser.city))
		print('{}{}'.format("\tState: ", currentUser.state))
		print('{}{}'.format("\tZip: ", currentUser.zip))


		allEvents = EventInfo.objects.filter(userProfile_id=userID).order_by('date')
		print(allEvents)
		mapping ={
			'currentUser' : currentUser,
			'allEvents': allEvents,


		}


	return render(request,'landingPage.html',mapping)


