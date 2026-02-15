from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    expected_delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_number = models.IntegerField()
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, default="Scheduled")

