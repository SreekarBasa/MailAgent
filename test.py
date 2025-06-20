import imaplib

with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
    EMAIL_USER='developer.14625@gmail.com'
    EMAIL_PASS='rhma keyg tcpz zdwe'
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    result, data = mail.uid('search', None, "UNSEEN")
    print("Unread UIDs:", data[0].split())