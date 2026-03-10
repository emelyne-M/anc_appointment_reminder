from django.db import models
from users.models import Patient


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

    created_at = models.DateTimeField(auto_now_add=True)


class Reminder(models.Model):

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=20)
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    scheduled_date = models.DateField(null=True)