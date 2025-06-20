# fastapi_routes.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mailapp.models import Email
import imaplib, email
from django.utils.timezone import make_aware
from datetime import datetime
from email.utils import parsedate_to_datetime
from django.conf import settings
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fastapi_app = FastAPI()

# Enable CORS to allow frontend requests from Django (adjust origins as needed)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def determine_priority(sender, subject, body):
    """Assign priority based on email content."""
    subject = subject.lower()
    sender = sender.lower()
    body = body.lower()
    if 'urgent' in subject or 'important' in subject:
        return 'high'
    if 'newsletter' in sender or 'promotional' in subject:
        return 'low'
    if 'meeting' in subject or 'schedule' in body:
        return 'medium'
    return 'low'

@fastapi_app.get("/check-new-mails")
def fetch_new_emails():
    """Fetch unread emails from Gmail and store them in the database."""
    logger.info("Fetching new emails...")
    try:
        # Use environment variables for sensitive credentials
        #EMAIL_USER = settings.EMAIL_USER
        #EMAIL_PASS = settings.EMAIL_PASS
        EMAIL_USER='developer.14625@gmail.com'
        EMAIL_PASS='rhma keyg tcpz zdwe'
        # Use context manager to ensure IMAP connection is properly closed
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL_USER, EMAIL_PASS)
            mail.select("inbox")

            # Search for unread emails
            result, data = mail.uid('search', None, "UNSEEN")
            uid_list = data[0].split()

            for uid in uid_list:
                result, msg_data = mail.uid('fetch', uid, '(RFC822)')
                raw = email.message_from_bytes(msg_data[0][1])

                subject = raw['Subject'] or ''
                sender = raw['From'] or ''
                # Robust date parsing using email.utils
                date = parsedate_to_datetime(raw['Date']) if raw['Date'] else make_aware(datetime.now())

                body = ''
                if raw.is_multipart():
                    for part in raw.walk():
                        if part.get_content_type() == 'text/plain':
                            body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                else:
                    body = raw.get_payload(decode=True).decode('utf-8', errors='ignore')

                # Avoid duplicate emails by checking UID
                if not Email.objects.filter(uid=uid.decode()).exists():
                    Email.objects.create(
                        uid=uid.decode(),
                        sender=sender,
                        subject=subject,
                        body=body,
                        date=date,
                        priority=determine_priority(sender, subject, body),
                        is_read=False
                    )

            logger.info(f"Processed {len(uid_list)} new emails.")
            return {"status": "New unread mails fetched and stored."}
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}")
        return {"status": "Error fetching emails", "error": str(e)}