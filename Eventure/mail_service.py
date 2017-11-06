import smtplib
from django.template import loader
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
#test receiver passed into mail_service
receivertest = 'juanromero2011@yahoo.com'
def mail_service(receiver):
   MY_ADDRESS = 'jromeutsa@gmail.com'
   PASSWORD = 'computerscience1'

   #addresses for texts
   # at&t 2101234567@mms.att.net
   # sprint 2101234567@pm.sprint.net
   # t-mobile 2101234567@tmomail.net
   # verizon 2101234567@vtext.net

   sender = 'jromeutsa@gmail.com'
   #receivers = 'juanromero2011@yahoo.com'
   receivers = receiver
   #test receivers = 'juanromero2011@yahoo.com','clwall95@gmail.com','ihankton123@yahoo.com',
             #   'alcortajuliana@yahoo.com','chyannef21@gmail.com']
   #txt_test receivers = '2108467265@pm.sprint.com', '6783387475@pm.sprint.com'

   message = """From: %s\nTo: %s\nSubject: %s\n\n%s
       """ % ("pyCharm~ "+MY_ADDRESS,     #Sender
              receiver,                   #Receiver
              "TEST SUBJECT",             #Subject
              "BODY TEST")                #Message

   try:
      mailServer = smtplib.SMTP('smtp.gmail.com', 587)
      mailServer.ehlo()
      mailServer.starttls()
      mailServer.login(MY_ADDRESS, PASSWORD)
      mailServer.sendmail(sender, receivers, message)
      print('Email Sent!')
   except smtplib.SMTPException:
      print('Error: email cannot be sent')

mail_service(receivertest) #call

recipientList =[]

def create_recipient_list(email):
   recipientList.append(email)

def sendEmailToAtendees(eventName, host):
   subject = '{host} has invited you to {eventName}'.format(host = host, eventName=eventName)
   html_message = loader.render_to_string('Eventure/Templates/displayEvent.html')
   text_content = strip_tags(html_message)
   msg = EmailMultiAlternatives(subject, text_content, recipientList)
   msg.attach_alternative(html_message, "text/html")
   msg.send()
   print (subject,recipientList)

