from pymongo import MongoClient, ASCENDING
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initialize the MongoDB database with collections and indexes'

    def handle(self, *args, **kwargs):
        client = MongoClient("mongodb+srv://nessa071390:Imp4l4013!@emrcapstone.5ocuvyf.mongodb.net/")
        db = client.EMRCapstone

        # Create indexes for collections
        db.users.create_index([("user_id", ASCENDING)], unique=True, name="user_id_index")
        db.patients.create_index([("patient_id", ASCENDING)], unique=True, name="patient_id_index")
        db.patients.create_index([("user_id", ASCENDING)], unique=True, name="user_id_index")
        db.doctors.create_index([("doctor_id", ASCENDING)], unique=True, name="doctor_id_index")
        db.doctors.create_index([("user_id", ASCENDING)], unique=True, name="user_id_index")
        db.nurses.create_index([("nurse_id", ASCENDING)], unique=True, name="nurse_id_index")
        db.nurses.create_index([("user_id", ASCENDING)], unique=True, name="user_id_index")
        db.office_administrators.create_index([("admin_id", ASCENDING)], unique=True, name="admin_id_index")
        db.office_administrators.create_index([("user_id", ASCENDING)], unique=True, name="user_id_index")
        db.medical_records.create_index([("record_id", ASCENDING)], unique=True, name="record_id_index")
        db.medical_notes.create_index([("note_id", ASCENDING)], unique=True, name="note_id_index")
        db.medical_notes.create_index([("medical_record_id", ASCENDING)], name="medical_record_id_index")
        db.appointments.create_index([("appointment_id", ASCENDING)], unique=True, name="appointment_id_index")
        db.appointments.create_index([("patient_id", ASCENDING)], name="patient_id_index")
        db.appointments.create_index([("doctor_id", ASCENDING)], name="doctor_id_index")

        self.stdout.write(self.style.SUCCESS('Database initialized successfully'))