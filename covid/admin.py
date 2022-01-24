from django.contrib import admin
from .models import Vaccine, Nurse, Patient, Vaccination_Record, Appointments

# Register your models here.
admin.site.register(Vaccine)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(Vaccination_Record)
admin.site.register(Appointments)
