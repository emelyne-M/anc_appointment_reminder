from django.db import models
from users.models import Patient
from django.utils import timezone


class Appointment(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    visit_number = models.IntegerField()

    scheduled_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('missed', 'Missed')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)

    def __str__(self):
        return f"{self.patient.full_name} - Visit {self.visit_number}"


class Reminder(models.Model):

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    reminder_type = models.CharField(
        max_length=10,
        choices=[
            ('SMS', 'SMS'),
            ('Email', 'Email')
        ]
    )

    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    