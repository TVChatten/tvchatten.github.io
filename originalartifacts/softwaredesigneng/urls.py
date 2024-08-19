from django.urls import path
from . import views

urlpatterns = [
    path('add_note/<int:patient_id>/', views.add_medical_note, name='add_medical_note'),
    path('view_record/<int:patient_id>/', views.view_medical_record, name='view_medical_record'),
    path('schedule_appointment/<int:doctor_id>/', views.schedule_appointment, name='schedule_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('edit_record/<int:record_id>/', views.edit_medical_record, name='edit_medical_record'),
    # Additional paths for user management
]