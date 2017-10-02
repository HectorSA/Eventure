from django.db import models
from django import forms
from django.contrib.auth.models import User
from localflavor.us.models import USStateField


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = 'user')
    id = models.AutoField(primary_key = True)
    firstName = models.CharField(max_length = 50, default = '')
    lastName = models.CharField(max_length = 50, default = '')
    #profilePhoto = models.ImageField(upload_to = 'profile_photos', blank = True, default = None)
    city = models.CharField(("city"), max_length=64)
    state = USStateField(("state"), default="TX")
    zip = models.CharField(("zip code"), max_length=5)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

class EventInfo(models.Model):
    id = models.CharField(primary_key = True, max_length = 12, default = '')
    userProfile = models.ForeignKey(UserProfile, null = True)
    type = models.BooleanField(default = False)  #auto-set to public
    name = models.CharField(max_length = 255, default = '')
    location = models.CharField(max_length = 255)
    date = models.DateField(null = True)
    time = models.TimeField(null = True)
    description = models.TextField()
    eventPhoto = models.ImageField(upload_to = 'event_photos', blank = True, default = None)


    def __str__(self):
        return '%s hosted by %s' % (self.name, self.host)


class Item(models.Model):
    itemID = models.AutoField(primary_key = True)
    eventID = models.ForeignKey(EventInfo, null = True)
    name = models.CharField(max_length = 255, default = '')
    amount = models.IntegerField(default = 0)
    isTaken = models.BooleanField(default = False)

    def __str__(self):
        return self.name + ' ' + self. amount




class Attendee(models.Model):
    NOTATTENDING = 1
    MAYBE = 2
    ATTENDING = 3
    
    RSVPSTATUS = (
        (NOTATTENDING, "Not Attending"),
        (MAYBE, "Maybe"),
        (ATTENDING, "Attending"),
        
    )
    
    attendeeName = models.CharField(max_length=256, default = '')
    attendeeID = models.CharField(max_length = 8, default = '')
    userAttendeeID = models.IntegerField(null = True)
    eventID = models.ForeignKey(EventInfo, null = True)
    itemID = models.ForeignKey(Item, null = True)
    email = models.EmailField(max_length=256, default='')
    RSVPStatus = models.IntegerField(choices=RSVPSTATUS, blank=True, null=True)