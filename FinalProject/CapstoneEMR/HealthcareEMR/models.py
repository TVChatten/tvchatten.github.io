from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, time, timedelta


class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Office Administrator'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_information = models.TextField()
    assigned_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    assigned_nurse = models.ForeignKey('Nurse', on_delete=models.SET_NULL, null=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_information = models.TextField()

    def __str__(self):
        return f'Dr. {self.first_name} {self.last_name}'

    def get_available_slots(self, date):
        slots = []
        start_time = datetime.combine(date, time(9, 0))  # Clinic starts at 9 AM
        end_time = datetime.combine(date, time(17, 0))   # Clinic ends at 5 PM
        delta = timedelta(minutes=30)

        while start_time < end_time:
            if not Appointment.objects.filter(doctor=self, appointment_date=start_time, is_booked=True).exists():
                slots.append(start_time)
            start_time += delta

        return slots

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nurse_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_information = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class OfficeAdministrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_information = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    #notes = models.ManyToManyField('MedicalNote', blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    date_of_record = models.DateField()

    def __str__(self):
        return f'Record {self.record_id} for {self.patient}'

class MedicalNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note_content = models.TextField()
    date_of_note = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Note {self.note_id} by {self.author} on {self.date_of_note}'

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #date = models.DateField()
    #time = models.TimeField()
    #status = models.CharField(max_length=20, choices=(('requested', 'Requested'), ('confirmed', 'Confirmed'), ('declined', 'Declined')))
    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment {self.appointment_id} with Dr. {self.doctor.last_name} for {self.patient.last_name if self.patient else "N/A"} on {self.appointment_date}'