import json
import smtplib

from email.mime.text import MIMEText


def send_email(event, context):

    body = json.loads(event['body'])

    recipient = body['recipient']

    subject = body['subject']

    message = body['message']

    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = recipient

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(
        '612ajaydudy@gmail.com',
        'buqf uqek vjdc smvv'
    )

    server.send_message(msg)

    server.quit()

    return {
        'statusCode': 200,
        'body': json.dumps('Email Sent Successfully')
    }