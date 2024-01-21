import imaplib
import email
from bs4 import BeautifulSoup
import os
from src.db import get_db

smtp_server = "imap.gmail.com"

sender_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def get_all_messages():
    # Connect to the SQLite database
    conn = get_db()
    cur = conn.cursor()

    # Execute the SELECT query to get all messages
    cur.execute('SELECT * FROM mails')

    # Fetch all rows
    rows = cur.fetchall()

    # Convert rows to a list of dictionaries
    messages = []
    for row in rows:
        # Get the column names from the cursor description
        column_names = [description[0] for description in cur.description]
        
        # Create a dictionary for each row
        message_dict = dict(zip(column_names, row))
        messages.append(message_dict)

    # Close the connection
    conn.close()

    return messages


def get_mails_in_inbox():
    messages = get_all_messages()

    return messages

    # with imaplib.IMAP4_SSL(smtp_server) as mail:
    #     mail.login(sender_email, password)
    #     status, messages = mail.select('"[Gmail]/Sent Mail"')

    #     for i in range(1, int(messages[0])):
    #         res, msg = mail.fetch(str(i), '(RFC822)')
    #         for response in msg:
    #             if isinstance(response, tuple):
    #                 msg = email.message_from_bytes(response[1])
    #                 b = msg
    #                 body = ""

    #                 if b.is_multipart():
    #                     for part in b.walk():
    #                         body = part.get_payload(decode=True)
    #                         if body:
    #                             soup = BeautifulSoup(body, "html.parser")
    #                             body = soup.find("p").get_text()
    #                 else:
    #                     body = b.get_payload(decode=True)
                        
                    
                    
    #                 inter_m = msg["Received"].split("\n")[2]
    #                 inter_m = inter_m.split(" ")
    #                 m = {
    #                     "mid": msg["Message-ID"],
    #                     "subject": msg["Subject"],
    #                     "receiver": inter_m[len(inter_m) - 1][1:-2],
    #                     "sender": msg["From"],
    #                     "date": msg["Date"],
    #                     "message": body.decode("utf-8") if type(body) == bytes else body
    #                 }

    #                 messages.append(m)
    # return messages[1:]