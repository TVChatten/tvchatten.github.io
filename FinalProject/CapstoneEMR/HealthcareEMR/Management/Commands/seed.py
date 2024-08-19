#The below code makes the entire program more secure.

from datetime import date, datetime
import os
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from models import Patient, Doctor, Nurse, OfficeAdministrator 
import getpass
import random
import string


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Function to generate a secure password if one is not provided
        def generate_secure_password(length=12):
            characters = string.ascii_letters + string.digits + string.punctuation
            secure_password = ''.join(random.choice(characters) for i in range(length))
            return secure_password

        # Function to generate the next available username based on a prefix
        def generate_username(prefix):
            existing_users = User.objects.filter(username__startswith=prefix).values_list('username', flat=True)
            max_number = 0
            for username in existing_users:
                match = re.match(r'^' + re.escape(prefix) + r'(\d+)$', username)
                if match:
                    max_number = max(max_number, int(match.group(1)))
            return f'{prefix}{max_number + 1}'

        # Function to create a user if it doesn't already exist
        def create_user(role_name):
            # Ask the user to input a username and check if it exists
            while True:
                username = input(f"Enter the {role_name}'s username (leave blank to auto-generate): ") or generate_username(role_name.lower())
                if not User.objects.filter(username=username).exists():
                    break
                print(f"Username '{username}' already exists. Please choose a different username.")

            # Prompt the user to input the password or generate one
            password = getpass.getpass(prompt=f"Enter password for {role_name} '{username}': ") or generate_secure_password()
            
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            return user

        # Create the Patient
        patient_user = create_user('Patient')

        # Prompt the user to input the date of birth only if the role is Patient
        date_of_birth = None
        if patient_user:
            while True:
                dob_input = input("Enter the patient's date of birth (YYYY-MM-DD): ")
                try:
                    date_of_birth = datetime.strptime(dob_input, '%Y-%m-%d').date()
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

        patient = Patient.objects.create(
            user=patient_user,
            first_name=input("Enter the patient's first name: "),
            last_name=input("Enter the patient's last name: "),
            date_of_birth=date_of_birth,
            contact_information=input("Enter the patient's contact information: ")
        )

        # Create the Doctor
        doctor_user = create_user('Doctor')
        doctor = Doctor.objects.create(
            user=doctor_user,
            first_name=input("Enter the doctor's first name: "),
            last_name=input("Enter the doctor's last name: "),
            specialization=input("Enter the doctor's specialization: ")
        )

        # Create the Nurse
        nurse_user = create_user('Nurse')
        nurse = Nurse.objects.create(
            user=nurse_user,
            first_name=input("Enter the nurse's first name: "),
            last_name=input("Enter the nurse's last name: ")
        )

        # Create the Office Administrator
        admin_user = create_user('Office Administrator')
        administrator = OfficeAdministrator.objects.create(
            user=admin_user,
            first_name=input("Enter the admin's first name: "),
            last_name=input("Enter the admin's last name: ")
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with secure user data and generated usernames.'))