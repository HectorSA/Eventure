import smtplib

MY_ADDRESS = 'jromeutsa@gmail.com'
PASSWORD = 'computerscience1'

#addresses for texts
# at&t 2101234567@mms.att.net
# sprint 2101234567@pm.sprint.net
# t-mobile 2101234567@tmomail.net
# verizon 2101234567@vtext.net

sender = 'jromeutsa@gmail.com'
receivers = 'juanromero2011@yahoo.com'
#test receivers = 'juanromero2011@yahoo.com','clwall95@gmail.com','ihankton123@yahoo.com',
          #   'alcortajuliana@yahoo.com','chyannef21@gmail.com']
#txt_test receivers = '2108467265@pm.sprint.com', '6783387475@pm.sprint.com'

message = """From: PyCharm~Juan <jromeutsa@gmail.com>
To: Receiever
Subject: FREE BOOZE 

This is a test email message .
"""

try:
   mailServer = smtplib.SMTP('smtp.gmail.com', 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.login(MY_ADDRESS, PASSWORD)
   mailServer.sendmail(sender, receivers, message)
   print('Email Sent!')
except:
   print('Error: email cannot be sent')