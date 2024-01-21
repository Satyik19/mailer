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
    for message in messages:
        count, replies = count_replies_and_update_db(message["mid"])
        message["replies"] = count
        message["reply"] = replies

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

def count_replies_and_update_db(original_message_id):
    # Connect to the IMAP server
    print(f"Message ID {original_message_id}")
    reply_count = 0
    replies = []
    with imaplib.IMAP4_SSL(smtp_server) as mail:
        # Login to the email account
        mail.login(sender_email, password)

        # Select the mailbox
        status, messages = mail.select("inbox")

        for i in range(1, int(messages[0])):
            res, msg = mail.fetch(str(i), '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # Check if the email is a reply to the original message
                    references = msg.get("References", "")
                    in_reply_to = msg.get("In-Reply-To", "")
                    

                    if original_message_id in references or original_message_id in in_reply_to:
                        reply_count += 1
                        b = msg
                        body = ""

                        if b.is_multipart():
                            for part in b.walk():
                                body = part.get_payload(decode=True)
                                if body:
                                    soup = BeautifulSoup(body, "html.parser")
                                    elem = soup.find("p")
                                    if elem:
                                        body = elem.get_text()
                        else:
                            body = b.get_payload(decode=True)
                            
                        
                        print(msg["To"])
                        inter_m = ""
                        if msg["To"]:
                            inter_m = msg["To"]
                        else:
                            inter_m = msg["Received"].split("\n")[2]
                            inter_m = inter_m.split(" ")
                            inter_m = inter_m[len(inter_m) - 1][1:-2]
                        
                        m = {
                            "mid": msg["Message-ID"],
                            "subject": msg["Subject"],
                            "receiver": inter_m,
                            "sender": msg["From"],
                            "date": msg["Date"],
                            "message": body.decode("utf-8") if type(body) == bytes else body
                        }
                        replies.append(m)
                    print (msg["subject"])

    # Update the count in the SQLite database
    update_reply_count_in_db(original_message_id, reply_count)
    return reply_count, replies

def update_reply_count_in_db(original_message_id, reply_count):
    # Connect to the SQLite database
    conn = get_db()
    cursor = conn.cursor()

    # Update the count in the mails table
    cursor.execute('UPDATE mails SET replies = ? WHERE mid = ?', (reply_count, original_message_id))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
