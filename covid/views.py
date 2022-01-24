from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.apps import apps
from .models import Appointments, Patient, Nurse, Vaccine, TimeSlot, Vaccination_Record




# Website Main Menu
def home(request):
    variables = {}

    return render(request, 'covid/home.html', variables)

#################
## Admin Views ##
#################

@login_required                                                            # Checks for login
@user_passes_test(lambda user: user.is_superuser, login_url='/covid/denied/')  # Checks for admin privileges
def adminMenu(request):
    variables = {}

    
    userModel = apps.get_model('accounts', 'User')
    variables["users"] = userModel.objects.all()

    return render(request, 'covid/admin/menu.html', variables)

def adminLink(request):
    variables = {}
    
    # userModel = apps.get_model('accounts', 'User')
    # variables["users"] = userModel.objects.all()

    return render(request, 'covid/admin/linktoadmin.html', variables)

def adminRegister(request):
    variables = {}
    print("inside adminRegister")

    if request.method == 'POST':
        # Get the model for User from account
        userModel = apps.get_model('accounts', 'User')

        ### User Account Information ###
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        user_name  = request.POST['username']
        email      = request.POST['email']
        password1  = request.POST['password1']
        password2  = request.POST['password2']

        # Count number of patients and add 1 for the patient number
        nurseNum = userModel.objects.filter(is_nurse=True).count() + 1
        if password1 != password2:
            variables["message"] = "Mismatched passwords."
        else:
            # Create a new user object to send to the database
            newNurseAccount = userModel.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=user_name,
                email=email,
                password=password1,
                is_nurse=True,
            )

            newNurseAccount.save()
            variables["message"] = f"{user_name} registered"

    return render(request, 'covid/admin/registernurse.html', variables)

def adminRepository(request):
    variables = {}
    vaccines = []

    # Query all vaccines
    vaccineQ = Vaccine.objects.all()

    # Store each vaccine type into array
    for currentVaccine in vaccineQ:
        vaccines.append(currentVaccine)

    variables['vaccines'] = vaccines

    return render(request, 'covid/admin/repository.html', variables)


def adminUpdateRepository(request):
    variables = {}

    if request.method == 'POST':
        vaccineName = request.POST.get('vaccine')
        numVaccines = int(request.POST.get('numVaccines'))

        # Confirm the existence of the vaccine
        try:
            selectedVaccine = Vaccine.objects.get(name=vaccineName)
            print("Valid Vaccine Requested")
        except ObjectDoesNotExist:
            print("Invalid Vaccine")
            return render(request, 'covid/admin/updateRepository.html', {'message' : "Invalid Vaccine"})

        # Confirm that the amount to remove doesn't exceed the number of vaccines on hold
        if selectedVaccine.dosesAvailible + numVaccines < 0:
            return render(request, 'covid/admin/updateRepository.html', {'message' : f"Selected amount to remove execeeds total vaccines in reserve"})
        
        # Update Repository
        selectedVaccine.dosesTotal += numVaccines
        selectedVaccine.dosesAvailible += numVaccines
        selectedVaccine.save()

        return render(request, 'covid/admin/updateRepository.html', {'message' : f"Updated {vaccineName}"})
        

    return render(request, 'covid/admin/updateRepository.html', variables)


#################
## Nurse Views ##
#################

# Helper Class
class NurseAppointment:
    def __init__(self, appointmentInstance): # __init__(self, ID, Appointment):
        self.crsfString = "{% csrf_token %}"
        self.AppointmentObject = appointmentInstance
        # Grab Date, Time lot, and Patient First and Last

        self.rowHTML = f"""
            <dt class="col-sm-3">{appointmentInstance.patient.fname} {appointmentInstance.patient.lname}</dt>
            <dd class="col-sm-9">
            <form action='/covid/nurse-menu/appointments/' method="post">
                Vaccine: {appointmentInstance.vaccination.name}, Date: {appointmentInstance.date}, Time Slot: {appointmentInstance.timeSlot}
                <input type="submit"   name="button{appointmentInstance.id}" value="Mark As Complete">
                <input type="submit"   name="cancel{appointmentInstance.id}" value="Cancel">
                </form>
            </dd>
        """


def nurseMenu(request):
    variables = {}
    
    # userModel = apps.get_model('accounts', 'User')
    # variables["users"] = userModel.objects.all()

    return render(request, 'covid/nurse/menu.html', variables)


@csrf_exempt # Except, otherwise I don't know how to get the CRSF token to verify properly in the string
def nurseAppointments(request):
    variables = {}
    appointmentRows = []

    ### Post Request ###
    if request.method == 'POST':
        # Locate Button ID of the button that was pressed
        appointmentID = 0
        option = "none"
        while True:
            if request.POST.get(f"button{appointmentID}"):
                option = "complete"
                break
            elif request.POST.get(f"cancel{appointmentID}"):
                option = "cancel"
                break
            appointmentID+= 1

        # Button ID Found
        if option == "complete":
            print(f"Complete {appointmentID} Pressed")
                        # Find corresponding appointment in database
            appointment = Appointments.objects.get(id=appointmentID)

            # Set firstDose attribute of patient depending on dose that they will recieve
            if appointment.patient.firstDose == "none":
                appointment.patient.firstDose = appointment.vaccination.name
                appointment.patient.save()
            elif appointment.patient.firstDose == "Pfizer":
                appointment.patient.firstDose = "Pfizer2"
                appointment.patient.save()
                

            # Create a vaccination record
            recordNum = Vaccination_Record.objects.all().count()
            Vaccination_Record.objects.create(
                # Primary Key
                id = recordNum,

                # Vaccination Details
                date = appointment.date,
                nurse = appointment.nurse,
                patient = appointment.patient,
                vaccine = appointment.vaccination
            ).save()

            # Update vaccine repository
            if appointment.vaccination.name == "Pfizer2":
                vaccineRecieved = Vaccine.objects.get(pk="Pfizer")
            else:
                vaccineRecieved = Vaccine.objects.get(name=appointment.vaccination.name)
            
            vaccineRecieved.dosesTotal -= 1
            vaccineRecieved.dosesOnHold -=1
            vaccineRecieved.save()

            # Update Nurse
            appointment.nurse.nPatients -= 1
            appointment.nurse.save()

            # Delete appointment
            appointment.delete()

        elif option == "cancel":
            print(f"Cancel {appointmentID} Pressed")
            appointment = Appointments.objects.get(pk=appointmentID)
            appointment.nurse.nPatients -= 1
            appointment.nurse.save()
            appointment.delete()
            variables['message'] = "Appointment Canceled"

   
    
    """
    # Get all current nurses appointments
    appointments = getAllAppointments where Nurse.ID = user.ID
    
    # For currAppointment in Appointment:
        # appointmentRows.append(Nurse_Appointment(i))
    """
    
    # Get the current nurses info
    currentNurseInfo = Nurse.objects.get(account=request.user)

    # Get all appointments associated with the current nurse
    appointmentsQ    = Appointments.objects.filter(nurse=currentNurseInfo)

    for appointment in appointmentsQ:
        appointmentRows.append(NurseAppointment(appointment))
    
    variables["appointmentRows"] = appointmentRows

    return render(request, 'covid/nurse/appointments.html', variables)

def nurseTimeSlots(request):
    variables = {}
    confirmationMessage = ""
    
    # Get Models

    ### Time Slow was Selected ###
    if request.method == 'POST':
        print("In POST")
        # Get the model for User from account
        currentAccount = request.user

        # Count number of patients and add 1 for the patient number
        currentNurseInfo = Nurse.objects.get(account= currentAccount)
       
        # Time Slot 1 
        if request.POST.get("timeSlot1"):
            print("Time Slot 1 Pressed")

            ### Update or Create Time Slot ###
            try:
                timeSlot = TimeSlot.objects.get(pk=1)
                print(timeSlot.nNurses)
                timeSlot.nNurses += 1
                timeSlot.save(update_fields=["nNurses"])
                print('Updated')
                print(timeSlot.nNurses)
            except TimeSlot.DoesNotExist:
                newTimeSlot = TimeSlot.objects.create(
                    hour = 1,
                    nNurses = 0
                )
                newTimeSlot.save()

            # Update the current nurses time slot to 1
            currentNurseInfo.timeSlot = 1
            currentNurseInfo.save()

            # Confirm Message
            confirmationMessage = "You are registered for time slot 1"
            
        # Time Slot 2
        elif request.POST.get("timeSlot2"):
            print("Time Slot 2 Pressed")

            try:
                timeSlot = TimeSlot.objects.get(pk=2)
                print(timeSlot.nNurses)
                timeSlot.nNurses += 1
                timeSlot.save(update_fields=["nNurses"])
                print('Updated')
                print(timeSlot.nNurses)
            except TimeSlot.DoesNotExist:
                newTimeSlot = TimeSlot.objects.create(
                    hour = 2,
                    nNurses = 0
                )
                newTimeSlot.save()
      
            # Update the current nurses time slot to 2
            currentNurseInfo.timeSlot = 2
            currentNurseInfo.save()


            # Confirm Message
            confirmationMessage = "You are registered for time slot 2"

        variables['message'] = confirmationMessage

    return render(request, 'covid/nurse/timeSlots.html', variables)



def viewInfo(request):
    currentUser = request.user
    nurseInfo = Nurse.objects.get(account = currentUser)
    #stud = Patient.objects.all()
    print("Myoutput", nurseInfo)
    stud = {'stu': nurseInfo }
    return render(request,'covid/nurse/viewInfo.html', stud)


def nurseUpdateInfo(request):

    variables = {}

    print("this is the issue")
    if request.method == 'POST':
        currentUser = request.user
        nurseInfo = Nurse.objects.get(account = currentUser)
        newAddress = request.POST['address']
        newPhoneNum = request.POST['phoneNum']

        nurseInfo.address = newAddress
        nurseInfo.phoneNum = newPhoneNum

        nurseInfo.save()

    return render(request,'covid/nurse/updateInfo.html', variables)


###################
## Patient Views ##
###################

def patientMenu(request):
    variables = {}
    
    # userModel = apps.get_model('accounts', 'User')
    # variables["users"] = userModel.objects.all()

    return render(request, 'covid/patient/patient_menu.html', variables)


def patientUpdateInfo(request):
    variables = {}

    return render(request, 'covid/patient/updatepatientinfo.html', variables)

# Helper Class
class PatientAppointmentCancel:
    def __init__(self, appointmentInstance): # __init__(self, ID, Appointment):
        self.crsfString = "{% csrf_token %}"
        self.AppointmentObject = appointmentInstance
        # Grab Date, Time lot, and Patient First and Last

        self.rowHTML = f"""
            <dt class="col-sm-3">{appointmentInstance.patient.fname} {appointmentInstance.patient.lname}</dt>
            <dd class="col-sm-9">
            <form action='/covid/patient-menu/viewSchedule/' method="post">
                Vaccine: {appointmentInstance.vaccination.name}, Date: {appointmentInstance.date}, Time Slot: {appointmentInstance.timeSlot}
                <input type="submit"   name="button{appointmentInstance.id}" value="Cancel">
                </form>
            </dd>
        """

@csrf_exempt
def patientViewAppointment(request):
     ### Post Request ###
    if request.method == 'POST':
        # Locate Button ID of the button that was pressed
        appointmentID = 0
        while not request.POST.get(f"button{appointmentID}"):
            appointmentID+= 1

        # Button ID Found
        print(f"Button {appointmentID} Pressed")

        # Find corresponding appointment in database
        appointment = Appointments.objects.get(id=appointmentID)

        # Update vaccine repository
        vaccineRecieved = Vaccine.objects.get(name=appointment.vaccination.name)
        vaccineRecieved.dosesAvailible +=1
        vaccineRecieved.dosesOnHold -=1
        vaccineRecieved.save()

        # Update 
        appointment.nurse.nPatients -= 1
        appointment.nurse.save()

        # Delete appointment
        appointment.delete()

    
    variables = {}
    appointmentRows = []
    
    """
    # Get all current nurses appointments
    appointments = getAllAppointments where Nurse.ID = user.ID
    
    # For currAppointment in Appointment:
        # appointmentRows.append(Nurse_Appointment(i))
    """
    
    # Get the current nurses info
    currentPatientInfo = Patient.objects.get(account=request.user)

    # Get all appointments associated with the current nurse
    appointmentsQ    = Appointments.objects.filter(patient=currentPatientInfo)

    for appointment in appointmentsQ:
        appointmentRows.append(PatientAppointmentCancel(appointment))
    
    variables["appointmentRows"] = appointmentRows

    return render(request, 'covid/patient/viewApps.html', variables)


def patientAppointment(request):
    print(request.method)
    # Returns user to schedule.html with an error message

    variables = {}

    # If the user has submitted a new registration
    print(f"The request method recieved was: {request.method}")
    userModel = apps.get_model('accounts', 'User')
    num = userModel.objects.filter(is_patient=True).count() + 1

    if request.method == 'POST':
        print(f"inside of post")
        currentUser = request.user
        patientInfo = Patient.objects.get(account = currentUser)
        
        ### User Account Information ###
        requestedTimeSlot = int(request.POST['timeSlot'])
        requestedVaccination = request.POST['vaccination']
        date = request.POST['date']
        
        # Check if the patient is eligible for a dose
        if patientInfo.firstDose in ["Moderna", "Pfizer2"]:
            return render(request, 'covid/patient/schedule.html', {'message' : "You have already completed your vaccination"})

        if patientInfo.firstDose == "Pfizer" and requestedVaccination == "Moderna":
            return render(request, 'covid/patient/schedule.html', {'message' : "You must schedule for your last Pfizer shot."})
        
        # Grab the requested time slot
        try:
            selectedTimeSlot = TimeSlot.objects.get(hour=requestedTimeSlot)
        except ObjectDoesNotExist:
            print("Invalid Time Slot")
            return render(request, 'covid/patient/schedule.html', {'message' : "Invalid Time Slot"})

        # Check if the requested vaccine is valid
        try:
            selectedVaccine = Vaccine.objects.get(name=requestedVaccination)
            print("Valid Vaccine Requested")
        except ObjectDoesNotExist:
            print("Invalid Vaccine")
            return render(request, 'covid/patient/schedule.html', {'message' : "Invalid Vaccine"})

        # Check if there is a valid range of nurses in the time slot
        nursesInTimeSlotQ = Nurse.objects.filter(timeSlot=requestedTimeSlot)
        nNurses = nursesInTimeSlotQ.count()
        print(f"Number of nurses in time slot {requestedTimeSlot}: {nNurses}")
        if nNurses < 1:
            return render(request, 'covid/patient/schedule.html', {'message' : "No nurses scheduled for that time slot"})

        # Find out which of the nurses in that time slot have less than 10 patients
        assignedNurse = None
        for currentNurse in nursesInTimeSlotQ:
            if currentNurse.nPatients < 10:
                print("A free nurse was found")
                assignedNurse = currentNurse
                break
        else:
            return render(request, 'covid/patient/schedule.html', {'message' : "All nurses are booked from that time slot"})

        nAppointments = Appointments.objects.all().count()
        newAppointment = Appointments.objects.create(
            id = nAppointments * 2,
            date=date,
            vaccination=selectedVaccine,
            timeSlot = requestedTimeSlot,
            patient = patientInfo,
            nurse = assignedNurse
        )

        newAppointment.save()

        # Update Repository
        selectedVaccine.dosesOnHold +=1
        selectedVaccine.dosesAvailible -=1
        selectedVaccine.save()

        # Update Nurse
        newAppointment.nurse.nPatients += 1
        newAppointment.nurse.save()

        return render(request, 'covid/patient/schedule.html', {'message' : "A new appointment was sucessfully created!"})

    return render(request, 'covid/patient/schedule.html', {'message' : ""})
    


def patientUpdateInfo(request):

    variables = {}

    if request.method == 'POST':
        currentUser = request.user
        patientInfo = Patient.objects.get(account = currentUser)
        newAddress = request.POST['address']
        newPhoneNum = request.POST['phoneNum']

        patientInfo.phoneNum = newPhoneNum
        patientInfo.address = newAddress

        patientInfo.save()

    return render(request,'covid/patient/editInfo.html', variables)

        
def patientInfo(request):
    currentUser = request.user
    patientInfo = Patient.objects.get(account = currentUser)
    #stud = Patient.objects.all()
    print("Myoutput", patientInfo)
    return render(request,'covid/patient/viewInfo.html',{'stu': patientInfo })
            
def patientRecord(request):
    variables = {}
    records = []
    currentUser = request.user
    patientInfo = Patient.objects.get(account = currentUser)

    recordQ = Vaccination_Record.objects.filter(patient=patientInfo)
    print(recordQ.count())

    for record in recordQ:
        records.append(record)

    variables['records'] = records

    return render(request,'covid/patient/record.html', variables)

#################
## Debug Views ##
#################

def debugMenu(request):
    confirmMessage = ""
    if request.method == 'POST':
        if request.POST.get('createPatient'):
            # Get the model for User from account
            userModel = apps.get_model('accounts', 'User')

            # Count number of patients and add 1 for the patient number
            patientNum = userModel.objects.filter(is_patient=True).count() + 1
            
            # Create a new user object to send to the database
            newPatientAccount = userModel.objects.create_user(
                first_name=f"patient{patientNum}_fname",
                last_name=f"patient{patientNum}_lname",
                username=f"patient{patientNum}",
                email=f"patient{patientNum}@patient.com",
                password="patient",
                is_patient=True,
            )

            # Save to database
            newPatientAccount.save()

            # Create Patient Entry in Database
            patientModel = apps.get_model('covid', 'Patient')
            newPatientInfo = patientModel.objects.create(
                # Primary Key
                ssn = patientNum * 2,
                
                # Patient's Account
                account = newPatientAccount,

                # Name
                fname   = f"patient{patientNum}_fname",
                mname   = f"patient{patientNum}_mname",
                lname   = f"patient{patientNum}_lname",

                # Vaccination Dose Info
                firstDose = "none",

                # General Info
                age        = patientNum,
                gender     = "M",
                race       = "race",
                occupation = "occupation",

                # Contact Info
                email    = f"patient{patientNum}@patient.com",
                address  = "address",
                phoneNum = "555-555-5555",
                
                # Medical History
                medHistory = "history",
            )
           
            confirmMessage = f" patient{patientNum} created\nusername: patient{patientNum}\npassword: patient \n"
            print(confirmMessage)

            newPatientInfo.save()

        elif request.POST.get('createNurse'):
            # Get the model for User from account
            userModel = apps.get_model('accounts', 'User')

            # Count number of patients and add 1 for the patient number
            nurseNum = userModel.objects.filter(is_nurse=True).count() + 1
            
            # Create a new user object to send to the database
            newNurseAccount = userModel.objects.create_user(
                first_name=f"nurse{nurseNum}_fname",
                last_name=f"nurse{nurseNum}_lname",
                username=f"nurse{nurseNum}",
                email=f"nurse{nurseNum}@patient.com",
                password="nurse",
                is_nurse=True,
            )

            newNurseAccount.save()
            
            # Get Nurse Model
            nurseModel = apps.get_model('covid', 'Nurse')
            
            # Populate Nurse Entry
            newNurseAccount = nurseModel.objects.create(
                # Primary Key
                id = nurseNum,

                # Nurse Account
                account = newNurseAccount,

                # Name
                fname   = f"nurse{nurseNum}_fname",
                mname   = f"nurse{nurseNum}_mname",
                lname   = f"nurse{nurseNum}_lname",

                # General Info
                age = nurseNum,
                gender = "M",

                # Contact Info
                phoneNum = "555-555-5555",
                address = "address"
            )

            newNurseAccount.save()

            confirmMessage = f" nurse{nurseNum} created\nusername: nurse{nurseNum}\npassword: nurse \n"
            print(confirmMessage)

    variables = {}
    variables['confirmMessage'] = confirmMessage

    return render(request, 'covid/debug/menu.html', variables)


#################
## Error Views ##
#################


def denied(request):
    variables = {}
    return render(request, 'covid/denied.html', variables)
