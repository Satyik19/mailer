import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils as utils
from .db import get_db
from datetime import datetime
import os

smtp_server = "smtp.gmail.com"
port = 465
sender_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def send_email(receiver_email, subject, msg):
    
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    mid = utils.make_msgid(domain="mailer-ok7r.onrender.com")
    message["Message-ID"] = mid

    html = f"""
<html>
<body>
    <p>{msg}</p>
    <img width="100px" height="100px" src="https://mailer-ok7r.onrender.com/image?mid={mid}" alt="">
</body>
</html>
"""

    # Attach the HTML content to the email
    message.attach(MIMEText(html, 'html'))
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.set_debuglevel(1)
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message.as_string())
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO mails (mid, subject, receiver, sender, date, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (mid, subject, receiver_email, sender_email, datetime.now(), msg))
    conn.commit()
    conn.close()


