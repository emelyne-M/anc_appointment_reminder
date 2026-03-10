from datetime import date
from .models import Appointment


def update_missed_appointments():

    today = date.today()

    missed = Appointment.objects.filter(
        scheduled_date__lt=today,
        status='pending'
    )

    for appointment in missed:
        appointment.status = 'missed'
        appointment.save()