from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name = 'user')
    id = models.AutoField(primary_key = True)
    firstName = models.CharField(max_length = 50, default = '')
    lastName = models.CharField(max_length = 50, default = '')
    #profilePhoto = models.ImageField(upload_to = 'profile_photos', blank = True, default = None)
    city = models.CharField(max_length = 50, default = '')
    state = models.CharField(max_length = 50, default = '')
    zip = models.IntegerField()

    def __str__(self):
        return self.firstName + ' ' + self.lastName


class Host(models.Model):
    user = models.OneToOneField(User, related_name = 'Host')

    def __str__(self):
        return self.user.firstName + ' ' + self.user.Last_name


class EventInfo(models.Model):
    id = models.AutoField(primary_key = True)
    host = models.ForeignKey(Host, null = True)
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


class Attendees(models.Model):
    name = models.OneToOneField(User,related_name = 'Attendee')
    attendeeID = models.ForeignKey(UserProfile, null = True)
    eventID = models.ForeignKey(EventInfo, null = True)
    itemID = models.ForeignKey(Item, null = True)