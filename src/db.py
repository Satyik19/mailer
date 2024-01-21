import sqlite3
from flask import g

DATABASE = 'mailer.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.cursor().execute("""CREATE TABLE IF NOT EXISTS mails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mid TEXT UNIQUE NOT NULL,
        subject TEXT NOT NULL,
        receiver TEXT NOT NULL,
        sender TEXT NOT NULL,
        date TEXT NOT NULL,
        message TEXT NOT NULL,
        count INTEGER DEFAULT 0,
        replies INTEGER DEFAULT 0,
        bounced BOOLEAN DEFAULT 0 
    )""")
    db.commit()
    db.close()
    