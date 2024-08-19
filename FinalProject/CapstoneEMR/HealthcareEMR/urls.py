from django.contrib import admin
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
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('patients/', views.patients_list, name='patients_list'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('nurses/', views.nurses_list, name='nurses_list'),
    path('medical-records/', views.medical_records_list, name='medical_records_list'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('administrators/', views.administrators_list, name='administrators_list'),
    path('request-appointment/', views.request_appointment, name='request_appointment'),
]