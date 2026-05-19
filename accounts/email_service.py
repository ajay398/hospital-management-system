import requests


def send_email(recipient, subject, message):

    url = "http://localhost:3000/dev/send-email"

    data = {
        "recipient": recipient,
        "subject": subject,
        "message": message
    }

    response = requests.post(url, json=data)

    return response.json()