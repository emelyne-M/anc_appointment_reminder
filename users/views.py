from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta

from .forms import SignUpForm, PatientForm
from appointments.models import Appointment, Reminder
from users.models import Patient

# -------------------------------
# SIGNUP
# -------------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        patient_form = PatientForm(request.POST)
        if form.is_valid() and patient_form.is_valid():
            user = form.save()
            patient = patient_form.save(commit=False)
            patient.user = user  # Link patient to user
            patient.save()

            # Automatically create ANC appointments based on EDD
            edd = patient.expected_delivery_date
            visit_weeks = [36, 32, 28, 24, 20, 16, 12, 8]
            for i, weeks_before in enumerate(visit_weeks, start=1):
                visit_date = edd - timedelta(weeks=weeks_before)
                Appointment.objects.create(
                    patient=patient,
                    visit_number=i,
                    scheduled_date=visit_date
                )

            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = SignUpForm()
        patient_form = PatientForm()

    return render(request, 'users/signup.html', {'form': form, 'patient_form': patient_form})


# -------------------------------
# LOGIN
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


# -------------------------------
# LOGOUT
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------
# DASHBOARD
# -------------------------------
def dashboard_view(request):
    total_patients = Patient.objects.count()
    today = date.today()

    # Today's visits and missed visits
    todays_visits = Appointment.objects.filter(scheduled_date=today).count()
    missed_visits = Appointment.objects.filter(scheduled_date__lt=today, status='pending').count()

    # SMS reminders sent today
    reminders_today = Reminder.objects.filter(sent_at__date=today).count()
    sms_status_sent = f"{reminders_today} sent"

    # For patient table: show if reminder sent
    patients = Patient.objects.all()
    patient_status_list = []

    for patient in patients:
        # Get upcoming appointment (next pending)
        upcoming = Appointment.objects.filter(patient=patient, status='pending').order_by('scheduled_date').first()
        if upcoming:
            reminder_sent = Reminder.objects.filter(appointment=upcoming, sent_at__date=today).exists()
            patient_status_list.append({
                'patient': patient,
                'upcoming_date': upcoming.scheduled_date,
                'reminder_sent': reminder_sent
            })
        else:
            patient_status_list.append({
                'patient': patient,
                'upcoming_date': None,
                'reminder_sent': False
            })

    return render(request, 'users/dashboard.html', {
        'total_patients': total_patients,
        'todays_visits': todays_visits,
        'missed_visits': missed_visits,
        'sms_status_sent': sms_status_sent,
        'patient_status_list': patient_status_list
    })
# -------------------------------
# SEND SMS REMINDERS (for cron/job)
# -------------------------------
def send_sms_reminders():
    from twilio.rest import Client
    import os

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    client = Client(account_sid, auth_token)

    tomorrow = date.today() + timedelta(days=1)
    appointments = Appointment.objects.filter(scheduled_date=tomorrow, status='pending')

    for appointment in appointments:
        patient = appointment.patient
        message = f"Hello {patient.full_name}, this is a reminder for your ANC Visit {appointment.visit_number} scheduled tomorrow."

        if twilio_number:
            client.messages.create(body=message, from_=twilio_number, to=patient.phone)
        else:
            print(f"[TEST] SMS to {patient.phone}: {message}")

        Reminder.objects.create(appointment=appointment, reminder_type='SMS')