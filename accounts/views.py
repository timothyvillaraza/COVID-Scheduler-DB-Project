from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.apps import apps
from .models import User

# Create your views here.
def accounts(request):
    return HttpResponse("<h1>accounts</h1>")


def login(request):
    variables = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            variables['error_message'] = 'Username/Password combination is incorrect'
            return render(request, 'accounts/login.html', variables)
    else:
        return render(request, 'accounts/login.html', variables)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    # TODO: Revamp Login? https://www.youtube.com/watch?v=Ev5xgwndmfc&list=PLzMcBGfZo4-kQkZp-j9PNyKq7Yw5VYjq9&index=9 @15 min in
    variables = {}

    # If the user has submitted a new registration
    print(f"The request method recieved was: {request.method}")
    if request.method == 'POST':
        # Post request argument is from the name= field in the register.html file
        
        ### User Account Information ###
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        user_name  = request.POST['username']
        email      = request.POST['email']
        password1  = request.POST['password1']
        password2  = request.POST['password2']

        ### Patient Info ###
        ssn = request.POST['ssn']
        middle_name = request.POST['middle_name']
        age = request.POST['age']
        gender = request.POST['gender']
        race = request.POST['race']
        occupation = request.POST['occupation']
        address = request.POST['address']
        phoneNum = request.POST['phoneNum']
        medHistory = request.POST['medHistory']

        
        # Check for integrity
        if password1 != password2:
            variables["error_message"] = "Mismatched passwords."
        elif User.objects.filter(email=email).exists():
            variables["error_message"] = "Email is in use."
        elif User.objects.filter(username=user_name).exists():
            variables["error_message"] = f"Username \"{user_name}\" is taken."
        else:
            # Create a new user object to send to the database
            newPatientAccount = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=user_name,
                email=email,
                password=password1,
                is_patient=True,
            )

            # Save to database
            newPatientAccount.save()

            # Create Patient Entry in Database
            patientModel = apps.get_model('covid', 'Patient')
            newPatientInfo = patientModel.objects.create(
                # Primary Key
                ssn = ssn,
                
                # Patient's Account
                account = newPatientAccount,

                # Name
                fname   = first_name,
                mname   = middle_name,
                lname   = last_name,

                # General Info
                age        = age,
                gender     = gender,
                race       = race,
                occupation = occupation,

                # Contact Info
                email    = email,
                address  = address,
                phoneNum = phoneNum,
                
                # Medical History
                medHistory = medHistory,
            )

            newPatientInfo.save()
            
            print("A new user was created")   
            return redirect('/')
          
    return render(request, 'accounts/register.html', variables)