from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
import random, string
from .forms import *
from .forms import userLoginForm
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse

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
	print("groupID:%s -- userID:%s -- website %s" % (groupID, userID, WEBSITENAME))


def index(request):
	return render(request, 'index.html', {})

################## /createEvent ###################
def createEvent(request):
	EmailFormSet = formset_factory(EmailInviteeForm)
	ItemFormSet = formset_factory(ItemForm)
	
	eventID = 0
	if request.method == 'POST':
		eventForm = CreateEventForm(request.POST,request.FILES)
		
		if eventForm.is_valid():
			eventID = createAlphanumericSequence(groupIDLength)
			userID = findUserID(request.user.id)
			eventType = eventForm.cleaned_data["type"]
			name = eventForm.cleaned_data["name"]
			location = eventForm.cleaned_data["location"]
			date = eventForm.cleaned_data["date"]
			time = eventForm.cleaned_data["time"]
			description = eventForm.cleaned_data["description"]
			#newEvent = EventInfo(eventID, userID, eventType, name,location, date, time, description)
						
			
			print('***********************************')
			print('{}{}'.format("Event: ", name))
			print('{}{}'.format("\tDUserID: ", request.user.id))
			print('{}{}'.format("\tUUserID: ", userID))
			print('{}{}'.format("\tType: ", eventType))
			print('{}{}'.format("\tLocation: ", location))
			print('{}{}'.format("\tDate: ", date))
			print('{}{}'.format("\tTime: ", time))
			print('{}{}'.format("\tDescription: ", description))
			print('{}{}'.format("\tEventID: ", eventID))
		
		inviteToEventFormset = EmailFormSet(request.POST, request.FILES, prefix='invitee')
		if inviteToEventFormset.is_valid():
			for invite in inviteToEventFormset:
				email = invite.cleaned_data["email"]
				print("\tEmail: " + email)
		
		
		itemCreationFormset = ItemFormSet(request.POST, request.FILES, prefix='item')
		if itemCreationFormset.is_valid():
			for item in itemCreationFormset:
				itemName = item.cleaned_data["itemName"]
				amount = item.cleaned_data["amount"]
				print('{}{}{}{}'.format("\tItem: ",itemName," x ",amount))

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

############################################################
def findUserID(djangoUserID):
	print(djangoUserID)
	applicationUser = UserProfile.objects.get(user_id=djangoUserID)
	print(applicationUser.id)
	return applicationUser.id

################userLogin(request)#########################
def userLogin(request):
	if request.method == 'POST':
		loginForm = userLoginForm(request.POST)
		print(loginForm)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			print(username)
			password = request.POST['password']
			print(password)
			user = authenticate(username=username, password=password)
			print(user)
			if user is not None:
				print("user is not none")
				if user.is_active:
					login(request, user)
					return render(request,'index.html')
				else:
					print("user is not Active")
					return render(request,'userLogin.html')
			else:
				print("user is none")
				loginForm = userLoginForm()
				return render(request,'userLogin.html',{'loginForm':loginForm})
	else:
		loginForm = userLoginForm()
		return render(request,'userLogin.html',{'loginForm':loginForm})

def userLogout(request):
	logout(request)
	return HttpResponseRedirect('/')