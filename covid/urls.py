from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # Home page in templates/covid/home
    path('', views.home, name='home'),
    
    # Admin Pages
    path('admin-menu/',    views.adminMenu,    name='admin-menu'),
    path('admin-menu/link-to-admin/',    views.adminLink,    name='admin-menu'),
    path('admin-menu/register-nurse/',    views.adminRegister,    name='admin-menu'),
    path('admin-menu/repository/',    views.adminRepository,    name='admin-menu'),
    path('admin-menu/updateRepository/',    views.adminUpdateRepository,    name='admin-menu'),

    # Nurse Pages
    path('nurse-menu/',    views.nurseMenu,    name='nurse-menu'),
    path('nurse-menu/viewInfo/',    views.viewInfo,    name='nurse-menu'),
    path('nurse-menu/update-info/',    views.nurseUpdateInfo,    name='nurse-menu'),
    path('nurse-menu/appointments/',    views.nurseAppointments,    name='nurse-appointments'),
    path('nurse-menu/time-slots/',    views.nurseTimeSlots,    name='nurse-time-slots'),

    # Patient Pages
    path('patient-menu/', views.patientMenu,    name = 'patient-menu'),
    path('patient-menu/viewInfo/', views.patientInfo,    name = 'patient-menu'),
    path('patient-menu/editInfo/', views.patientUpdateInfo,    name = 'patient-menu'),
    path('patient-menu/viewSchedule/', views.patientViewAppointment,    name = 'patient-menu'),
    path('patient-menu/schedule/', views.patientAppointment,    name = 'patient-menu'),
    path('patient-menu/record/', views.patientRecord,    name = 'patient-menu'),

    # Debug Pages
    path('debug/', views.debugMenu, name = 'debug-menu'),
    
    # Error Pages
    path('denied/', views.denied, name='denied')
]
