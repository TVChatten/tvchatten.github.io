from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from models import Patient, Doctor, Nurse, OfficeAdministrator
from datetime import date
import string
import random

class SeedDataTestCase(TestCase):

    def generate_random_username(self, prefix):
        """Generates a random and secure username with a given prefix."""
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{prefix}{suffix}"

    def generate_secure_password(self, length=12):
        """Generates a secure password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def test_patient_creation(self):
        # Generate secure username and password
        username = self.generate_random_username('patient')
        password = self.generate_secure_password()

        # Create a patient user
        user = User.objects.create_user(username=username, password=password)
        patient = Patient.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            contact_information='123 Main St'
        )

        # Assertions
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(patient.user.username, username)
        self.assertEqual(patient.first_name, 'John')
        self.assertEqual(patient.date_of_birth, date(1990, 1, 1))

    def test_doctor_creation(self):
        # Generate secure username and password
        username = self.generate_random_username('doctor')
        password = self.generate_secure_password()

        # Create a doctor user
        user = User.objects.create_user(username=username, password=password)
        doctor = Doctor.objects.create(
            user=user,
            first_name='Jane',
            last_name='Smith',
            specialization='Cardiology'
        )

        # Assertions
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(doctor.user.username, username)
        self.assertEqual(doctor.specialization, 'Cardiology')

    def test_nurse_creation(self):
        # Generate secure username and password
        username = self.generate_random_username('nurse')
        password = self.generate_secure_password()

        # Create a nurse user
        user = User.objects.create_user(username=username, password=password)
        nurse = Nurse.objects.create(
            user=user,
            first_name='Nina',
            last_name='Brown'
        )

        # Assertions
        self.assertEqual(Nurse.objects.count(), 1)
        self.assertEqual(nurse.user.username, username)
        self.assertEqual(nurse.first_name, 'Nina')

    def test_office_admin_creation(self):
        # Generate secure username and password
        username = self.generate_random_username('admin')
        password = self.generate_secure_password()

        # Create an office administrator user
        user = User.objects.create_user(username=username, password=password)
        admin = OfficeAdministrator.objects.create(
            user=user,
            first_name='Alice',
            last_name='Johnson'
        )

        # Assertions
        self.assertEqual(OfficeAdministrator.objects.count(), 1)
        self.assertEqual(admin.user.username, username)
        self.assertEqual(admin.first_name, 'Alice')

    def test_username_generation_uniqueness(self):
        # Generate two users with the same prefix to ensure unique usernames
        username1 = self.generate_random_username('testuser')
        username2 = self.generate_random_username('testuser')
        password1 = self.generate_secure_password()
        password2 = self.generate_secure_password()

        user1 = User.objects.create_user(username=username1, password=password1)
        user2 = User.objects.create_user(username=username2, password=password2)

        # Ensure the usernames are unique
        self.assertNotEqual(user1.username, user2.username)

    def test_date_of_birth_patient_only(self):
        # Create a patient and ensure date of birth is set
        patient_username = self.generate_random_username('patient')
        patient_password = self.generate_secure_password()
        user_patient = User.objects.create_user(username=patient_username, password=patient_password)
        patient = Patient.objects.create(
            user=user_patient,
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            contact_information='123 Main St'
        )

        # Create a doctor and ensure date of birth is not set
        doctor_username = self.generate_random_username('doctor')
        doctor_password = self.generate_secure_password()
        user_doctor = User.objects.create_user(username=doctor_username, password=doctor_password)
        doctor = Doctor.objects.create(
            user=user_doctor,
            first_name='Jane',
            last_name='Smith',
            specialization='Cardiology'
        )

        # Assertions
        self.assertEqual(patient.date_of_birth, date(1990, 1, 1))
        self.assertFalse(hasattr(doctor, 'date_of_birth'))