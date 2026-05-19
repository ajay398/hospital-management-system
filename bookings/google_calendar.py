from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build

from google.auth.transport.requests import Request

import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():

    creds = None

    if os.path.exists('token.pkl'):

        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def create_calendar_event(slot, patient):

    service = get_calendar_service()

    start_datetime = f"{slot.date}T{slot.start_time}"

    end_datetime = f"{slot.date}T{slot.end_time}"

    event = {

        'summary': f'Appointment with {patient.username}',

        'description': 'Hospital Appointment',

        'start': {
            'dateTime': start_datetime,
            'timeZone': 'Asia/Kolkata',
        },

        'end': {
            'dateTime': end_datetime,
            'timeZone': 'Asia/Kolkata',
        },
    }

    service.events().insert(
        calendarId='primary',
        body=event
    ).execute()