
from django.template import loader, RequestContext, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core import mail
from django.conf import settings
from django.utils.html import strip_tags
##import html2text

#global variable for recipient list
recipientList =[]
emaiLinkDict = {}
items = []

def create_recipient_list(email, emailLink):
   recipientList.append(email)
   emaiLinkDict.update({email:emailLink})

def sendEmailToAtendees(eventObject):
    connection = mail.get_connection()
    connection.open()
    subject = "You Have been invited to: " + eventObject.name
    for attendeeEmail in recipientList:
        message = 'Hey, ' + attendeeEmail + ' you have been invited to: ' + eventObject.name + '\nClick on the link to set your RSVP status:\n' + emaiLinkDict.get(attendeeEmail)
        email = EmailMessage(subject,message, settings.DEFAULT_FROM_EMAIL,[attendeeEmail],connection=connection)
        email.send()
    connection.close()

def sendItemsEmailUpdate(attendeeEmail,hostName, eventName,itemName):
    connection = mail.get_connection()
    connection.open()
    subject = "Item Modification"
    message = "Hello we are sorry to inform you that: "+ hostName+" has changed the item: '"+ itemName + " for event: "+ eventName +"\nAs a result of the change you have been automatically unsigned up for the item: "+ itemName+"\n"
    email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL, [attendeeEmail],connection=connection)
    email.send()
    connection.close()