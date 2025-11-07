from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment
from accounts.models import User

class AppointmentForm(forms.ModelForm):
    lawyer = forms.ModelChoiceField(queryset=User.objects.filter(role='lawyer'))
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'min': (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
                'class': 'form-control'
            }
        ),
        label='Appointment Date & Time'
    )

    class Meta:
        model = Appointment
        fields = ['lawyer', 'date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your case or reason for consultation...'}),
        }

    def clean_date(self):
        d = self.cleaned_data['date']
        if d <= timezone.now():
            raise forms.ValidationError("Please choose a future date and time.")
        return d
