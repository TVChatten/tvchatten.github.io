from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from models import Patient, Doctor, Nurse, MedicalRecord, Appointment, OfficeAdministrator, MedicalNote
from datetime import date

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create Users
        user1 = User.objects.create_user(username='patient1', password='password123')
        user2 = User.objects.create_user(username='doctor1', password='password123')
        user3 = User.objects.create_user(username='nurse1', password='password123')
        user4 = User.objects.create_user(username='admin1', password='password123')

        # Create Patient
        patient = Patient.objects.create(
            user=user1,
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            contact_information='123 Main St'
        )

        # Create Doctor
        doctor = Doctor.objects.create(
            user=user2,
            first_name='Alice',
            last_name='Smith',
            specialty='Cardiology',
            contact_information='456 Elm St'
        )

        # Create Nurse
        nurse = Nurse.objects.create(
            user=user3,
            first_name='Robin',
            last_name='Brown',
            contact_information='789 Oak St'
        )

        # Assign Doctor and Nurse to Patient
        patient.assigned_doctor = doctor
        patient.assigned_nurse = nurse
        patient.save()

        # Create Medical Record
        medical_record = MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,
            nurse=nurse,
            diagnosis='Hypertension',
            treatment='Medication',
            date_of_record=date(2023, 1, 1)
        )

        # Create Medical Note
        medical_note = MedicalNote.objects.create(
            medical_record=medical_record,
            author=doctor.user,
            note_content='Patient needs to follow up in 6 months.'
        )

        # Create Appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=None,
            reason='Routine checkup',
            is_booked=False
        )

        # Create Office Administrator
        admin = OfficeAdministrator.objects.create(
            user=user4,
            first_name='Office',
            last_name='Admin',
            contact_information='admin@example.com'
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))