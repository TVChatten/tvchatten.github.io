from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MedicalRecord, MedicalNote, Appointment, User, Doctor, Patient, Nurse, OfficeAdministrator
from .forms import MedicalNoteForm, AppointmentForm, EditMedicalRecordForm
from .utils import calculate_penalty
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError

#Permissions to add a record if you're a nurse or a doctor.
@login_required
def add_medical_note(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.user.role == 'doctor' or request.user.role == 'nurse':
        if request.method == 'POST':
            form = MedicalNoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.created_by = request.user
                note.save()
                patient.medical_records.notes.add(note)
                return redirect('view_medical_record', patient_id=patient.id)
        else:
            form = MedicalNoteForm()
        return render(request, 'add_medical_note.html', {'form': form, 'patient': patient})
    else:
        return redirect('home')
    
#Permissions to view a record
@login_required
def view_medical_record(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    medical_records = patient.medical_records.all()
    return render(request, 'view_medical_record.html', {'patient': patient, 'medical_records': medical_records})

#Permissions to schedule an appointment
@login_required
def schedule_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.doctor = doctor
            if form.cleaned_data['time'] in doctor.available_times.get(str(form.cleaned_data['date']), []):
                appointment.status = 'confirmed'
            else:
                appointment.status = 'declined'
            appointment.save()
            return redirect('view_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'schedule_appointment.html', {'form': form, 'doctor': doctor})

#Permissions to view an appointment
@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'view_appointments.html', {'appointments': appointments})

#Permissions for the office administrator to manage the users
@login_required
def manage_users(request):
    if request.user.role == 'admin':
        users = User.objects.all()
        return render(request, 'manage_users.html', {'users': users})
    else:
        return redirect('home')
    
#Permissions for a doctor to edit the medical record    
@login_required
def edit_medical_record(request, record_id):
    medical_record = get_object_or_404(MedicalRecord, id=record_id)
    
    if request.user.role == 'doctor':
        if request.method == 'POST':
            form = EditMedicalRecordForm(request.POST, instance=medical_record)
            if form.is_valid():
                form.save()
                return redirect('view_medical_record', patient_id=medical_record.patient.id)
        else:
            form = EditMedicalRecordForm(instance=medical_record)
        return render(request, 'edit_medical_record.html', {'form': form, 'medical_record': medical_record})
    else:
        return redirect('home')


# Additional views for creating, updating, and deleting users

def home(request):
    return render(request, 'home.html')

def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients_list.html', {'patients': patients})

def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})

def nurses_list(request):
    nurses = Nurse.objects.all()
    return render(request, 'nurses_list.html', {'nurses': nurses})

def medical_records_list(request):
    medical_records = MedicalRecord.objects.all()
    return render(request, 'medical_records_list.html', {'medical_records': medical_records})

def appointments_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments_list.html', {'appointments': appointments})

def administrators_list(request):
    administrators = OfficeAdministrator.objects.all()
    return render(request, 'administrators_list.html', {'administrators': administrators})

def request_appointment(request):
    if request.method == 'POST':
        try:
            #Retrieves form data
            patient_id = request.POST['patient_id']
            doctor_id = request.POST['doctor_id']
            preferred_datetime_str = request.POST['preferred_datetime']
            reason = request.POST['reason']

            #Parsing out the preferred datetime
            preferred_datetime = datetime.strptime(preferred_datetime_str, '%Y-%m-%d %H:%M')

            #Patient and Doctor Objects
            patient = Patient.objects.get(patient_id=patient_id)
            doctor = Doctor.objects.get(doctor_id=doctor_id)

            #Get available slots for inputted data 
            available_slots = doctor.get_available_slots(preferred_datetime.date())

            #If no available slots, return an error
            if not available_slots:
                return JsonResponse({'status': 'error', 'message': 'No available slots'})
            
            #Calculate the best slot based on penalty
            best_slot = min(available_slots, key=lambda slot: calculate_penalty(preferred_datetime, slot))
            penalty = calculate_penalty(preferred_datetime, best_slot)


            #If the penalty is too high, return an error
            if penalty > 3600:  # 1 hour penalty threshold
                return JsonResponse({'status': 'error', 'message': 'No suitable slots within acceptable range'})
            
            #Create and book the appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=best_slot,
                reason=reason,
                is_booked=True
            )

            return JsonResponse({'status': 'success', 'message': 'Appointment booked', 'appointment_id': appointment.appointment_id})
    
        except ObjectDoesNotExist as oer:
             # Handle case where the patient or doctor does not exist
            return JsonResponse({'status': 'error', 'message': 'Patient or Doctor does not exist: ' + str(oer)})
        except ValidationError as ver:
            # Handle validation errors
            return JsonResponse({'status': 'error', 'message': 'Validation error: ' + str(ver)})
        except Exception as exr:
            # Handle any other unexpected errors
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred: ' + str(exr)})
        
    # Retrieve patients and doctors for the form
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'request_appointment.html', {'patients': patients, 'doctors': doctors})