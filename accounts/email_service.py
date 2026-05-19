import requests


SERVERLESS_URL = "http://localhost:3000/dev/send-email"


def send_email(recipient, subject, message):

    payload = {
        "recipient": recipient,
        "subject": subject,
        "message": message
    }

    requests.post(
        SERVERLESS_URL,
        json=payload
    )