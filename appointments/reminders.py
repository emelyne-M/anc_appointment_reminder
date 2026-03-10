from datetime import date, timedelta
from twilio.rest import Client
from .models import Appointment, Reminder
import os

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

def send_sms_reminders():
    tomorrow = date.today() + timedelta(days=1)
    appointments = Appointment.objects.filter(scheduled_date=tomorrow, status='pending')

    for appointment in appointments:
        patient = appointment.patient
        message = f"Hello {patient.full_name}, this is a reminder for your Antenatal care Visit {appointment.visit_number} scheduled tomorrow."
        # Send SMS
        # Use console print for testing if no Twilio number
        if twilio_number:
            client.messages.create(body=message, from_=twilio_number, to=patient.phone)
        else:
            print(f"[TEST] SMS to {patient.phone}: {message}")
        # Log reminder
        Reminder.objects.create(appointment=appointment, reminder_type='SMS')
        print(f"Reminder sent to {patient.full_name}")