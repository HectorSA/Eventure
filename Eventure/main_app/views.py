from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response
import random, string
from .forms import *
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse

WEBSITENAME = 'Eventure'


# Create your views here.


def register(request):
    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(request.POST)
        user_profile_form = UserProfile(request.POST)

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


def createEvent(request):
    EmailFormSet = formset_factory(EmailInviteeForm)
    ItemFormSet = formset_factory(ItemForm)
    eventForm = CreateEventForm()

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


def createURL():
    eventID = createAlphanumericSequence(10)
    userID = createAlphanumericSequence(6)

    print(eventID + userID)


############################################################


################userLogin(request)#########################
def userLogin(request):
    if (request.method == 'POST'):
        loginForm = userLoginForm(data=request.POST)
        userName = request.POST['userName']
        password = request.POST['password']
        user = authenticate(userName=userName, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('index.html')
    loginForm = userLoginForm()
    return render(request, 'userLogin.html', {'loginForm': loginForm})
