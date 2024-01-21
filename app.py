from flask import Flask, request, send_file, render_template
from src.send_mail import send_email
from src.mail_dashboard import get_mails_in_inbox
from src.db import init_db, get_db
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
init_db()


@app.route("/api/send", methods=["POST"])
def send_emails():
    data = request.get_json()
    print(data)
    receiver = data.get("receiver", "")
    subject = data.get("subject", "")
    message = data.get("message", "")
    send_email(receiver_email=receiver, subject=subject, msg=message)
    return {"status": "success"}

@app.route("/image", methods=["GET"])
def send_image():
    mid = request.args.get("mid")
    print(mid)
    if mid is None:
        return send_file("output.png")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE mails SET count = count + 1 WHERE mid = ?', (mid,))
    conn.commit()
    conn.close()

    return send_file("./output.png")

@app.route("/api/all", methods=["GET"])
def get_mails():
    m = get_mails_in_inbox()
    print(m)
    return m

@app.route("/")
def home():
    return send_file("./static/index.html")