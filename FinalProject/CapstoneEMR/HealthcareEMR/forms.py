from django import forms
from .models import MedicalNote, Appointment, MedicalRecord

class MedicalNoteForm(forms.ModelForm):
    class Meta:
        model = MedicalNote
        fields = ['content']

class EditMedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['notes']
        widgets = {
            'notes': forms.CheckboxSelectMultiple,
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']