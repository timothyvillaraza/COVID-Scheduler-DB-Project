from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Vaccine(models.Model):
    # Primary Key
    name = models.TextField(primary_key=True)           # Brand Name

    # General Info                                      
    company       = models.TextField()                  # Company
    desc          = models.TextField()                  # Optional
    requiredDoses = models.IntegerField(default=1)      # 1, 2, or more doses required?

    # Supply Information
    dosesTotal     = models.IntegerField()
    dosesOnHold    = models.IntegerField()
    dosesAvailible = models.IntegerField()


class Nurse(models.Model):
    # Primary Key
    id = models.IntegerField(primary_key=True)

    # User Account
    account = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=-1)

    # Name
    fname   = models.TextField()
    mname   = models.TextField()
    lname   = models.TextField()
    
    # General Info
    age     = models.IntegerField()
    gender  = models.TextField()

    # Contact Info
    phoneNum = models.TextField()
    address  = models.TextField()

    # Time Slot Info
    timeSlot  = models.IntegerField(default=-1)
    nPatients = models.IntegerField(default=0)


class Patient(models.Model):
    # Primary Key
    ssn = models.IntegerField(primary_key=True)

    # Patient's Account
    account = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=-1)

    # Name
    fname   = models.TextField() 
    mname   = models.TextField() 
    lname   = models.TextField() 

    # Vaccination Info (Probably just use operations to count # of patient doses from vaccination records)
    firstDose  = models.TextField(default="none") # Pfizer, get Pfizer again?

    # General Info
    age        = models.IntegerField() 
    gender     = models.TextField()    
    race       = models.TextField()    
    occupation = models.TextField()    

    # Contact Info
    email    = models.EmailField(max_length = 200) 
    address  = models.TextField()
    phoneNum = models.TextField()

    # Medical History
    medHistory = models.TextField()


# TODO: Find out how to implement
class Vaccination_Record(models.Model):
    # Primary Key
    id = models.IntegerField(primary_key=True)

    # Vaccination Details
    date    = models.TextField()
    nurse   = models.ForeignKey(Nurse,   on_delete=models.PROTECT, default=-1)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, default=-1)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT, default=-1)


class Appointments(models.Model):
    # Primary Key
    id = models.IntegerField(primary_key=True)

    # Appointment Details
    timeSlot   = models.TextField(default = '10am') # Parse Int Later
    date        = models.TextField()
    vaccination = models.ForeignKey(Vaccine, on_delete=models.PROTECT, default=-1)

    # People involved in appointment - If nurse or patient is gone, so is the appointment
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    nurse   = models.ForeignKey(Nurse,   on_delete=models.PROTECT)


class TimeSlot(models.Model):
    # Primary Key
    hour    = models.IntegerField(primary_key=True)

    # Number of nurses in timeslot
    nNurses = models.IntegerField(default=0)
