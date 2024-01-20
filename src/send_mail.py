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
    html = f"""
<html>
<body>
    <p>{msg}</p>
    <img width="100px" height="100px" src="https://img.freepik.com/free-vector/realistic-hand-drawn-fuck-you-symbol_23-2148684365.jpg?w=740&t=st=1705778735~exp=1705779335~hmac=b2ba99e51f7f27d170217c8318b28beca6fda407c1c1a81959a19324222df681" alt="Tracking Pixel">
</body>
</html>
"""
    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    mid = utils.make_msgid(domain="localhost")
    message["Message-ID"] = mid

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


