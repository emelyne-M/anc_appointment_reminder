from rest_framework import serializers
from .models import Patient
from datetime import date

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_expected_delivery_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Expected delivery date cannot be in the past!")
        return value