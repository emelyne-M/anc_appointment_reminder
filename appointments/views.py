from rest_framework import viewsets
from .models import Appointment
from users.models import Patient
from .serializers import AppointmentSerializer, PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer