import smtplib
from django.template import loader, RequestContext
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags

#global variable for recipient list
recipientList =[]

def create_recipient_list(email):
   recipientList.append(email)

def sendEmailToAtendees(eventName, host, request):
   subject = '{host} has invited you to {eventName}'.format(host = host, eventName=eventName)
   html_message = loader.render_to_string('displayEvent.html')
   text_content = "This is the text_content"
   msg = EmailMultiAlternatives(subject, html_message, recipientList)
   msg.content_subtype = "html"
   msg.send()
   print (subject,recipientList)

