import smtplib
from django.template import loader, RequestContext, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core import mail
from django.utils.html import strip_tags
##import html2text

#global variable for recipient list
recipientList =[]
emaiLinkDict = {}
items = []


def create_recipient_list(email, emailLink):
   recipientList.append(email)
   emaiLinkDict.update({email:emailLink})

def itemsPerEvent(item):
   items.append(item)

def sendEmailToAtendees(eventObject, newEmailInvitee , host, request):
    connection = mail.get_connection()
    connection.open()
    subject = '{host} has invited you to {eventName}'.format(host = host, eventName=eventObject.name)
    content = {'eventInfo':eventObject,
               'items':items,
               'guests': newEmailInvitee}
    for attendeeEmail in recipientList:
        email = EmailMessage(subject,emaiLinkDict.get(attendeeEmail), recipientList)
        email.send()

    connection.close()
    print (subject,recipientList, content)
    #text_content = "This is the Text content"
    #html_message = loader.render_to_string('displayEvent.html', content)
    #print(text_content)
    #msg = EmailMultiAlternatives(subject, html_message, recipientList)
    #msg.content_subtype = "html"
    #smsg.send()

