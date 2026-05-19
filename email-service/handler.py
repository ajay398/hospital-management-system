import json
import smtplib
import os

from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(event, context):

    body = json.loads(event['body'])

    recipient = body['recipient']
    subject = body['subject']
    message = body['message']

    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = recipient

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(
        EMAIL_USER,
        EMAIL_PASSWORD
    )

    server.send_message(msg)

    server.quit()

    return {
        'statusCode': 200,
        'body': json.dumps('Email Sent Successfully')
    }