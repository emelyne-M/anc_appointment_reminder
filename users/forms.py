from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient

# User signup form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Patient form to store extra info
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('full_name', 'phone', 'expected_delivery_date')
        widgets = {
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'})
        }