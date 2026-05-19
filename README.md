# hospital-management-system
# Mini Hospital Management System (HMS)

A backend-focused Hospital Management System built using Django, PostgreSQL, Google Calendar API, and a separate Serverless Email Notification Service.

This project was developed as part of a backend engineering shortlisting task.

---

# Features

## Authentication
- Doctor and Patient signup/login
- Session-based authentication
- Password hashing
- Role-based access control

---

## Doctor Features
- Create availability slots
- View own slots
- Delete slots
- Manage bookings

---

## Patient Features
- View doctors
- View available slots
- Book appointments
- View booking history

---

## Appointment Booking
- Prevents double booking
- Race condition handling using:
  - `transaction.atomic()`
  - `select_for_update()`

---

## Google Calendar Integration
- Google OAuth2 authentication
- Automatic calendar event creation after booking

---

## Serverless Email Service
- Separate serverless email service
- Built using:
  - Serverless Framework
  - serverless-offline
  - Python SMTP
- Sends:
  - SIGNUP_WELCOME email
  - BOOKING_CONFIRMATION email

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Django | Backend Framework |
| PostgreSQL | Database |
| Django ORM | Database ORM |
| Google Calendar API | Calendar Integration |
| Serverless Framework | Email Service |
| Gmail SMTP | Email Sending |
| Python | Backend Language |
| HTML | Templates |

---

# Project Structure

```bash
hospital-management-system/
│
├── accounts/
├── bookings/
├── doctors/
├── patients/
├── templates/
├── email-service/
│   ├── handler.py
│   ├── serverless.yml
│   └── requirements.txt
│
├── ai-tool-usage-log/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Setup and Run

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPO_LINK
```

---

## 2. Create Virtual Environment

```bash
python -m venv env
```

Activate environment:

### Windows

```bash
env\Scripts\activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4. Setup PostgreSQL

Create database:

```sql
CREATE DATABASE hms_db;
```

---

## 5. Configure Database

Update `hms/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hms_db',
        'USER': 'postgres',
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 8. Run Django Server

```bash
python manage.py runserver
```

Django runs on:

```text
http://127.0.0.1:8000/
```

---

# Google Calendar Setup

## 1. Create Google Cloud Project

Enable:
- Google Calendar API

---

## 2. Create OAuth Credentials

Download:

```text
credentials.json
```

Place in project root.

---

## 3. First Booking

First booking triggers OAuth login.

Google token is stored locally in:

```text
token.pkl
```

---

# Serverless Email Service Setup

## 1. Go To Email Service

```bash
cd email-service
```

---

## 2. Install Dependencies

```bash
npm install
```

Install serverless globally:

```bash
npm install -g serverless
```

---

## 3. Start Serverless Offline

```bash
serverless offline
```

Runs on:

```text
http://localhost:3000/dev/send-email
```

---

# System Architecture

## Django HMS Backend
Handles:
- authentication
- role-based access
- slot management
- booking logic
- Google Calendar integration

---

## PostgreSQL Database
Stores:
- users
- doctor slots
- bookings

---

## Serverless Email Service
A separate serverless application responsible only for email sending.

Django communicates with the service using HTTP requests.

---

## Google Calendar Integration
After successful booking:
1. Booking created
2. Slot locked
3. Calendar event created
4. Confirmation email sent

---

# The Design Decision

## Problem
How to prevent two patients from booking the same slot simultaneously.

---

## Option 1
Use only:

```python
if slot.is_booked:
```

### Problem
Two requests arriving at the same time could still book the same slot.

---

## Option 2 (Chosen)
Use database-level locking:

```python
transaction.atomic()
select_for_update()
```

---

## Why I Chose This
This approach locks the database row during the transaction and guarantees only one booking operation can modify the slot at a time.

This is safer and more reliable for concurrent booking systems.

---

# Limitations

## Current Limitations

- Google Calendar currently uses one authenticated account locally
- No Docker support
- No async task queue
- No production deployment
- Minimal frontend styling
- No Redis caching

---

## Production Improvements

- Separate OAuth tokens per user
- Docker containerization
- Celery + Redis for async emails
- JWT authentication
- Better UI/UX
- Cloud deployment

---

# Future Improvements

- Multi-user Google Calendar synchronization for both doctors and patients
- Real-time notifications using WebSockets
- Video consultation integration
- Payment gateway integration for appointment fees
- Doctor profile management with specialization and experience
- Appointment cancellation and rescheduling
- SMS notifications using Twilio
- Admin analytics dashboard
- JWT authentication for API security
- Docker containerization and cloud deployment
- AI-based appointment recommendation system
- Medical report upload and management
- Role-based permission enhancements
- Appointment approval workflow with pending/rejected states
- Email reminders before appointments

---

# AI Tool Usage

AI tools were used during development for:
- Django backend guidance
- Google Calendar integration
- Serverless architecture guidance
- PostgreSQL setup
- Debugging support

AI-generated suggestions were manually reviewed, tested, and modified during implementation.

<!-- Note  -->
Current implementation creates Google Calendar events
through authenticated HMS calendar integration.
Architecture supports extension to multi-user OAuth
for doctor/patient-specific calendar synchronization.

---

# Author

Ajay Kumar