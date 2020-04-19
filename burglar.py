"""
This is a burglar alarm. It sends email with picture,
when it detects motion.
18-Apr-2020 by Roosa Wederhorn
"""

import smtplib, ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import os
import re

def main():
    port = 465
    password = getpass.getpass("Type the sender email password and press enter: ")
    
    m = open("./email.txt", "r")
    if m.mode == 'r':
       ml = m.readlines()
       m.close()

    message = MIMEMultipart("alternative")
    linectr = 0
    match = re.search(r"[Ss]ender[eE]mail: ([\w.-]+@[\w.-]+)",ml[linectr])
    if match: senderEmail = match.group(1)
    else: print("Sender email not found. Please review the email source file.")
    linectr += 1

    match = re.search(r"[Rr]eceiver[Ee]mail: ([\w.-]+@[\w.-]+)",ml[linectr])
    if match: receiverEmail = match.group(1)
    else: print("Receiver email not found. Please review the email source file.")
    linectr += 1

    match = re.search(r"[Ss]ubject: (.+)",ml[linectr])
    if match: subject = match.group(1)
    else: print("Subject not found. Please review the email source file.")
    linectr += 1

    message["Subject"] = subject
    message["From"] = senderEmail
    message["To"] = receiverEmail
    
    if re.search(r"[Ee]mail",ml[linectr]): 
        linectr += 1
        text = "".join(ml[linectr:]) 
    else: print("Email not found. Please review the email source file.")
    
    image = open("./veneily.jpg", 'rb').read()

    text = MIMEText(text,"plain","utf-8")
    image = MIMEImage(image, name=os.path.basename("./veneily.jpg"))
    message.attach(text)
    message.attach(image)

# Create secure SSL context
    context = ssl.create_default_context()
# Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("ebinbenis0@gmail.com", password)
        server.sendmail(senderEmail, receiverEmail, message.as_string())

if __name__ == "__main__":
    main()
