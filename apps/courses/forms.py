from django import forms
from django.core.validators import RegexValidator
from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    # --- CUSTOM VALIDATORS ---
    # Only letters (a-z, A-Z) and spaces allowed
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message="Full Name must only contain letters."
    )

    # Only digits (0-9) allowed
    numbers_only = RegexValidator(
        regex=r'^\d+$',
        message="WhatsApp Number must only contain digits."
    )

    # Letters and numbers allowed (No symbols/punctuation)
    alphanumeric = RegexValidator(
        regex=r'^[a-zA-Z0-9]+$',
        message="This field must be alphanumeric (letters and numbers only)."
    )

    # --- FORM FIELDS ---
    full_name = forms.CharField(
        max_length=20,
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'placeholder': 'ENTER FULL NAME',
            'class': 'form-control',
            'style': 'text-transform: uppercase;'
        })
    )

    index_number = forms.CharField(
        min_length=10,
        max_length=10,
        validators=[alphanumeric],
        widget=forms.TextInput(attrs={
            'placeholder': '10-CHARACTER INDEX',
            'class': 'form-control',
            'style': 'text-transform: uppercase;'
        })
    )

    whatsapp_number = forms.CharField(
        min_length=10,
        max_length=10,
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            'placeholder': '02XXXXXXXX',
            'class': 'form-control',
            'type': 'tel'
        })
    )

    reference_id = forms.CharField(
        validators=[alphanumeric],
        widget=forms.TextInput(attrs={
            'placeholder': 'TRANSACTION ID',
            'class': 'form-control',
            'style': 'text-transform: uppercase;'
        })
    )

    # Required field that must be checked to proceed
    payment_confirmed = forms.BooleanField(
        required=True,
        label="I confirm that I have sent the payment and the Reference ID is correct.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Enrollment
        fields = ['full_name', 'index_number', 'whatsapp_number', 'reference_id']

    # --- AUTO-UPPERCASE LOGIC ---
    # This ensures data is converted to UPPERCASE before saving to database

    def clean_full_name(self):
        data = self.cleaned_data.get('full_name')
        return data.upper() if data else ""

    def clean_index_number(self):
        data = self.cleaned_data.get('index_number')
        return data.upper() if data else ""

    def clean_reference_id(self):
        data = self.cleaned_data.get('reference_id')
        return data.upper() if data else ""