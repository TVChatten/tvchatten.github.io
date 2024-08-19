from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord, MedicalNote, Appointment, User, Doctor, Patient, Nurse, OfficeAdministrator
from .forms import MedicalNoteForm, AppointmentForm, EditMedicalRecordForm

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

@login_required
def view_medical_record(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    medical_records = patient.medical_records.all()
    return render(request, 'view_medical_record.html', {'patient': patient, 'medical_records': medical_records})

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

@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'view_appointments.html', {'appointments': appointments})

@login_required
def manage_users(request):
    if request.user.role == 'admin':
        users = User.objects.all()
        return render(request, 'manage_users.html', {'users': users})
    else:
        return redirect('home')
    
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