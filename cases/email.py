import smtplib
from email.message import EmailMessage
from utils.ai_utils import generate_email_from_intent
from config import GMAIL_EMAIL, APP_PASSWORD, TO_EMAIL, EMAIL_SUBJECT

def run(page):
    intent = input("What email do you want to send? ")
    EMAIL_BODY=generate_email_from_intent(intent)
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = GMAIL_EMAIL
    msg['To'] = TO_EMAIL
    msg.set_content(EMAIL_BODY)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)
    