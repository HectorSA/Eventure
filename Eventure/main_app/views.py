from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import DetailView
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
from datetime import date

WEBSITENAME = 'Eventure'
groupIDLength = 12
userIDLength = 8
from django.views import View

# Create your views here.
def anonymousUserMapping(attendee, eventInfo, eventId):
	rsvpStatus = getRSVPStatus(attendee.RSVPStatus)
	address = getParsedEventAddr(eventInfo.id)
	guests = Attendee.objects.filter(eventID=eventInfo.id, RSVPStatus=3)
	items = Item.objects.filter(eventID=eventInfo.id)
	print(attendee.RSVPStatus)
	return {
		'attendee': attendee,
		'eventInfo': eventInfo,
		'address': address,
		'rsvpStatus': rsvpStatus,
		'guests':guests,
		'items': items,
	}

def registeredUserMapping(request, eventInfo):
	mapping = {}
	user = User.objects.get(id = request.user.id)
	address = getParsedEventAddr(eventInfo.id)
	guests = Attendee.objects.filter(eventID=eventInfo.id,RSVPStatus=3).order_by("attendeeName")
	items = Item.objects.filter(eventID=eventInfo.id)
	attendee = Attendee
	for guest in guests:
		if(guest.email is request.user.email):
			attendee = guest
	rsvpStatus = getRSVPStatus(attendee.RSVPStatus)
	items = Item.objects.filter(eventID=eventInfo.id)
	mapping = {
		'eventInfo':eventInfo,
		'rspvStatus':rsvpStatus,
		'address': address,
		'guests': guests,
		'items': items,
	}
	return mapping

def setRsvpStatus(request, attendee):
	if request.POST.get("ATTENDING"):
		setattr(attendee, "RSVPStatus", 3)
	elif request.POST.get("MAYBE"):
		setattr(attendee, "RSVPStatus", 2)
	elif request.POST.get("NOTATTENDING"):
		setattr(attendee, "RSVPStatus", 1)
	attendee.save()


class attendeeEventDisplay(View):
	template_name = 'displayEvent.html'
	userId = UserProfile
	eventInfo = EventInfo
	attendee = Attendee
	groupId = ''
	attendeeId = ''
	def get(self,request, *args):
		argList = list(args)
		print(len(argList))
		if(len(argList) >= 2):
			self.groupId = argList[0]
			self.attendeeId = argList[1]
			self.eventInfo = EventInfo.objects.get(id=self.groupId)
			self.attendee = Attendee.objects.get(attendeeID=self.attendeeId)
			mapping = anonymousUserMapping(self.attendee,self.eventInfo, self.groupId)
			return render(request, self.template_name, mapping)
		elif(len(argList) == 1):
			self.groupId = argList[0]
			self.eventInfo = EventInfo.objects.get(id=self.groupId)
			mapping = registeredUserMapping(request, self.eventInfo)
			return render(request, self.template_name, mapping)

	def post(self, request, *args, **kwargs):
		argList = list(args)
		if (len(argList) >= 2):
			self.groupId = argList[0]
			self.attendeeId = argList[1]
			self.eventInfo = EventInfo.objects.get(id=self.groupId)
			self.attendee = Attendee.objects.get(attendeeID=self.attendeeId)
		else:
			self.groupId = argList[0]
			self.eventInfo = EventInfo.objects.get(id=self.groupId)
		setRsvpStatus(request, self.attendee)
		groupId = args[0]
		self.eventInfo = EventInfo.objects.get(id=groupId)
		rsvpStatus = getRSVPStatus(getattr(self.attendee,"RSVPStatus"))
		print(rsvpStatus)
		guests = Attendee.objects.filter(eventID=groupId, RSVPStatus=3)
		items = Item.objects.filter(eventID=groupId)
		address = getParsedEventAddr(self.eventInfo.id)
		mapping = {
			'attendee': self.attendee,
			'eventInfo': self.eventInfo,
			'address': address,
			'rsvpStatus': rsvpStatus,
			'guests': guests,
			'items': items,
		}
		return render(request, self.template_name, mapping)

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

def displayEventForExistentUser(request,groupID, userID):
	currentEvent = EventInfo.objects.filter(id=groupID)
	user = UserProfile.objects.filter(id=request.user.id)

# Used to display an event from a URL given to anon users from an email
def displayEvent(request, groupID, userID):
	currentEvent = EventInfo.objects.filter(id = groupID)
	attendee = findAttendee(userID)
	rsvpStatus = getRSVPStatus(attendee.RSVPStatus)
	address = getParsedEventAddr(groupID)
	guests = Attendee.objects.filter(eventID=groupID, RSVPStatus=3)
	items = Item.objects.filter(eventID=groupID)
	if(request.method == 'GET'):
		if(currentEvent is not None):
			if(attendee is not None):
				print(rsvpStatus)
				mapping = {
					'attendee':getattr(attendee,"attendeeName"),
					'currentEvent':currentEvent,
					'address':address,
					'rsvpStatus':rsvpStatus,
					'guests':guests,
					'items':items,
				}
				return render(request, 'displayEvent.html', mapping)
			else:
				pass
	elif(request.method == 'POST'):
		print(request.method)
		if(attendee is not None):
			if request.POST.get("ATTENDING"):
				setattr(attendee,"RSVPStatus",3)
			elif request.POST.get("MAYBE"):
				setattr(attendee, "RSVPStatus", 2)
			elif request.POST.get("NOTATTENDING"):
				setattr(attendee, "RSVPStatus", 1)
			rsvpStatus = getRSVPStatus(getattr(attendee,"RSVPStatus"))
			mapping = {
				'attendee': attendee,
				'currentEvent': currentEvent,
				'address': address,
				'rsvpStatus': rsvpStatus,
				'guests': guests,
				'items': items,
			}
			return render(request, 'displayEvent.html', mapping)

def index(request):
	return render(request, 'index.html', {})

def newIndex(request):
	if request.method == 'GET':
		publicEvents = getAllPublicEvents()
		print(publicEvents)
		mapping = {
			'publicEvents' : publicEvents,
			'media_url' : settings.MEDIA_URL + 'event_photos/'
		}
		return render(request, 'newIndex.html', mapping)

################## /createEvent ###################
def createEvent(request):
	if not request.user.is_authenticated():
		return	HttpResponseRedirect('/')
	
	EmailFormSet = formset_factory(EmailInviteeForm)
	ItemFormSet = formset_factory(ItemForm)
	
	## This is the eventID that will be assigned to email invitees
	eventID = 0
	newEvent = None
	if request.method == 'POST':
		eventForm = CreateEventForm(request.POST,request.FILES)
		
		if eventForm.is_valid():
			eventID = createAlphanumericSequence(groupIDLength)
			creatingUser = findUser(request.user.id)
			eventType = eventForm.cleaned_data["type"]
			name = eventForm.cleaned_data["name"]
			location = eventForm.cleaned_data["location"]
			date = eventForm.cleaned_data["date"]
			time = eventForm.cleaned_data["time"]
			description = eventForm.cleaned_data["description"]
			eventCategory = eventForm.cleaned_data["eventCategory"]
			
			newEvent = EventInfo(id = eventID, userProfile = creatingUser, type = eventType,
								 name = name, location = location, date = date,
								 time = time, description = description,
								 eventCategory = eventCategory)
			if 'eventPhoto' in request.FILES:
				newEvent.eventPhoto = request.FILES['eventPhoto']
			else:
				newEvent.eventPhoto = getDefaultPicture(eventCategory)
				print("DEFAULT\n\n")
			newEvent.save()
			printEventInfo(newEvent)
			
		
		inviteToEventFormset = EmailFormSet(request.POST, prefix='invitee')
		if inviteToEventFormset.is_valid():
			for invite in inviteToEventFormset:
				if invite.has_changed():
					emailUserID = createAlphanumericSequence(userIDLength)
					email = invite.cleaned_data["email"]
					userAttendeeID = -1

					foundUser = findUserViaEmail(email)
					if(foundUser):
						userAttendeeID = foundUser.id
					
					newEmailInvitee = Attendee(attendeeName=email, attendeeID=emailUserID,
				                           eventID=newEvent, email=email, RSVPStatus=1,
				                           userAttendeeID=userAttendeeID)
					## Printing
					emailLink = createInviteLink(newEvent, newEmailInvitee)
					print('{}{}'.format("\t", emailLink))
					
					## Saving
					newEmailInvitee.save()
		
		itemCreationFormset = ItemFormSet(request.POST, prefix='item')
		if itemCreationFormset.is_valid():
			for item in itemCreationFormset:
				if item.has_changed():
					itemName = item.cleaned_data["itemName"]
					itemAmount = item.cleaned_data["amount"]

					newItem = Item(eventID = newEvent, name = itemName, amount = itemAmount)
					
					printItemInfo(newItem)
					newItem.save()
				
		if eventForm.is_valid():
			print('***********************************')
			return HttpResponseRedirect('/landingPage')
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
					return HttpResponseRedirect('/')				
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
		currentUser = findUser(request.user.id)
		userID = currentUser.id
		
		allEvents = EventInfo.objects.filter(userProfile_id=userID).order_by('date')
		attendees = Attendee.objects.filter(userAttendeeID=userID)

		mapping ={
			'currentUser' : currentUser,
			'allEvents': allEvents,
			'media_url': settings.MEDIA_URL + 'event_photos/',
			'attendees': attendees,
		}

	return render(request,'landingPage.html',mapping)


def eventHomePageView(request,groupID):
	print('test')
	
	instance = EventInfo.objects.get(id=groupID)
	currentEvent = EventInfo.objects.get(id=groupID)
	guests = Attendee.objects.filter(eventID=groupID, RSVPStatus=3)
	items = Item.objects.filter(eventID=groupID)
	
	mapping = {
		'currentEvent': currentEvent,
		'guests': guests,
		'items': items,
		# 'itemCreationFormset': itemCreationFormset,
	}
	print(currentEvent.type)
	if request.user.is_authenticated():  # if they are a user
		currentUser = findUser(request.user.id)
		if currentUser == instance.userProfile:
			print(currentUser)
			return render(request, 'hostEventHomePage.html', mapping)
		elif currentEvent.type == False:
			return render(request, 'eventHomePage.html', mapping)
		else:
			print(currentEvent.type)
			return render(request,'thisIsPrivate.html')
	elif currentEvent.type == False:
		return render(request, 'eventHomePage.html', mapping)
	else:
		return render(request, 'thisIsPrivate.html')

############################## Edit ##########################################
def edit(request,groupID):
	instance = EventInfo.objects.get(id=groupID)
	if request.user.is_authenticated():
		currentUser = findUser(request.user.id)
		print(currentUser)
		print(instance.userProfile)
		
		if currentUser == instance.userProfile:
			currentEvent = EventInfo.objects.get(id=groupID)
			print(currentEvent.type)
			guests = Attendee.objects.filter(eventID=groupID, RSVPStatus=3)
			items = Item.objects.filter(eventID=groupID)
			invited = Attendee.objects.filter(eventID=groupID)
			ItemFormSet = formset_factory(ItemForm)
			newItem = ItemForm(request.POST)
			
			print(request.user.id)
			print(instance)
			form = CreateEventForm(request.POST or None, request.FILES or None, instance=instance)
				
				
			if request.method == 'POST':
				if form.is_valid():
					form.save()
					print('{}'.format("valid form"))
					newurl = '/event/' + currentEvent.id
					#test
					return HttpResponseRedirect(newurl)
					
					
				#itemCreationFormset = ItemFormSet(request.POST, prefix='item')
				'''####if itemCreationFormset.is_valid():
					for item in itemCreationFormset:
						if item.has_changed():
							itemName = item.cleaned_data["itemName"]
							itemAmount = item.cleaned_data["amount"]
							print('{}{}{}{}'.format("\tItem: ", itemName, " x ", itemAmount))
							newItem = Item(eventID=groupID, name=itemName, amount=itemAmount)
							newItem.save()
					print("test")
					print(newItem)
					return HttpResponseRedirect('/landingPage')####'''
				'''if newItem.is_valid():
					itemName = newItem.cleaned_data["itemName"]
					itemAmount = newItem.cleaned_data["amount"]
					print('{}{}{}{}'.format("\tItem: ", itemName, " x ", itemAmount))
					nnewItem = Item(eventID=currentEvent, name=itemName, amount=itemAmount)
					nnewItem.save()'''
				
				mapping = {
					'currentEvent': currentEvent,
					'guests': guests,
					'items': items,
					'form': form,
					'invited': invited,
					'newItem': newItem,
					#'itemCreationFormset': itemCreationFormset,
				}
				return render(request, 'editEvent.html', mapping)
			else:
					##inviteToEventFormset = EmailFormSet(prefix='invitee')
				#itemCreationFormset = ItemFormSet(prefix='item')
				mapping = {
					'currentEvent': currentEvent,
					'guests': guests,
					'items': items,
					'form': form,
					'invited': invited,
					'newItem': newItem,
					#'itemCreationFormset': itemCreationFormset,
				}
			return render(request, 'editEvent.html', mapping)
		return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

######################## None View Functions #################################
###############################################################################
################### createInviteLink #################
def createInviteLink(eventObject, AttendeeObject):
	print('{}'.format(AttendeeObject.attendeeName))
	
	emailLink = "http://127.0.0.1:8000/event/" + eventObject.id + AttendeeObject.attendeeID
	return emailLink


################## Print Event Info ##################
def printEventInfo(eventObject):
	if (eventObject):
		print('{}'.format("*****************************************"))
		print('{}'.format("************** Event Info ***************"))
		print('{}{}'.format("**\tEvent Name: ", eventObject.name))
		print('{}{}'.format("**\tEvent Creater: ", eventObject.userProfile))
		print('{}{}'.format("**\tLocation: ", eventObject.location))
		print('{}{}'.format("**\tDate: ", eventObject.date))
		print('{}{}'.format("**\tTime: ", eventObject.time))
		print('{}{}'.format("**\tDescription: ", eventObject.description))
		print('{}{}'.format("**\tType: ", eventObject.type))
		print('{}{}'.format("**\tCategory: ", eventObject.get_eventCategory_display()))
		print('{}{}'.format("**\tEventID: ", eventObject.id))
		print('{}'.format("*****************************************"))
	else:
		print('{}'.format("************ Event Info *************"))
		print('{}'.format("\tnil"))
		print('{}'.format("*************************************"))


################## Print Item Info ##################
def printItemInfo(itemObject):
	if (itemObject):
		print('{}'.format("************** Item Info ***************"))
		print('{}{}'.format("\tItem: ", itemObject))
		print('{}{}'.format("\tEvent ID: ", itemObject.eventID.id))
		print('{}{}'.format("\tItem ID: ", itemObject.itemID))
		print('{}{}'.format("\tIs Taken: ", itemObject.isTaken))
		print('{}'.format("*****************************************"))
	else:
		print('{}'.format("************ Event Info *************"))
		print('{}'.format("\tnil"))
		print('{}'.format("*****************"))


def printAttendeeInfo(attendeeObject):
	if (attendeeObject):
		print('{}'.format("************** Event Info ***************"))
		print('{}{}'.format("\tAttendee Name: ", attendeeObject.attendeeName))
		print('{}{}'.format("\tAttendee ID: ", attendeeObject.attendeeID))
		print('{}{}'.format("\tAttendee User ID: ", attendeeObject.userAttendeeID))
		print('{}{}'.format("\tAttendee Event ID: ", attendeeObject.eventID.id))
		print('{}{}'.format("\tAttendee Email: ", attendeeObject.email))
		print('{}{}'.format("\tAttendee RSVP Status: ", attendeeObject.RSVPStatus))
		print('{}'.format("*****************************************"))
	else:
		print('{}'.format("************ Event Info *************"))
		print('{}'.format("\tnil"))
		print('{}'.format("*****************"))


################# Functions used by views #################
# Will return a string of specified length of alphanumeric characters
def createAlphanumericSequence(sequenceLength):
	alphaNumericSequence = ''.join(random.choice(string.ascii_letters + string.digits)
	                               for digits in range(sequenceLength))
	return alphaNumericSequence


###############getParsedEventAddress###################
def getParsedEventAddr(groupId):
	valueList = EventInfo.objects.filter(id=groupId).values_list('location', flat=True)
	newList = []
	newList.insert(0, "query=")
	newList.extend(valueList[0])
	i = 0
	for value in newList:
		if (value.isspace()):
			newList[i] = "+"
		i = i + 1
	address = ''.join(str(s) for s in newList)
	print(address)
	return address


####################get public events ###################
def getAllPublicEvents():
	eventInfo = EventInfo.objects.filter(type=False).filter(date__gte=(date.today())).order_by('date')
	return eventInfo


####################get RSVP status ###################
def getRSVPStatus(rsvpNumber):
	NOTATTENDING = 1
	MAYBE = 2
	ATTENDING = 3
	
	RSVPSTATUS = {
		NOTATTENDING: "not attending",
		MAYBE: "undecided",
		ATTENDING: "attending"
	}
	return RSVPSTATUS[rsvpNumber]


################### findGroup ########################
def findUserViaEmail(emailAddress):
	try:
		eventureUser = UserProfile.objects.get(user__email=emailAddress)
	except UserProfile.DoesNotExist:
		eventureUser = None
	return eventureUser


################### findGroup ########################
def findGroup(groupID):
	eventInfo = EventInfo.objects.filter(id=groupID)
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


################# getDefaultPicture ####################
def getDefaultPicture(eventCategory):
	if (eventCategory == 0):
		return "event_photos/defaultimgs/nothingEventGeneric.jpg"
	elif (eventCategory == 1):
		return "event_photos/defaultimgs/partyEventGeneric.jpg"
	elif (eventCategory == 2):
		return "event_photos/defaultimgs/educationEventGeneric.jpg"
	elif (eventCategory == 3):
		return "event_photos/defaultimgs/musicEventGeneric.jpg"
	elif (eventCategory == 4):
		return "event_photos/defaultimgs/fooddrinkEventGeneric.jpg"
	elif (eventCategory == 5):
		return "event_photos/defaultimgs/moviesEventGeneric.jpg"
	elif (eventCategory == 6):
		return "event_photos/defaultimgs/artEventGeneric.jpg"
	elif (eventCategory == 7):
		return "event_photos/defaultimgs/technologyEventGeneric.jpg"
	elif (eventCategory == 8):
		return "event_photos/defaultimgs/healthEventGeneric.jpg"
	elif (eventCategory == 9):
		return "event_photos/defaultimgs/outdoorsEventGeneric.jpg"
	elif (eventCategory == 10):
		return "event_photos/defaultimgs/sportsEventGeneric.jpg"
	else:
		return "event_photos/defaultimgs/noneEventGeneric.jpg"