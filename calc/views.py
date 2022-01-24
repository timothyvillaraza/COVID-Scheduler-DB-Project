from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def calcView(request):
    variables = {}
    return render(request, 'calc.html', variables)


def add(request):
    variables = {}
    
    # Get input from calc.html form submission
    # All GET/POST functions return a string
    num1Input = int(request.POST['num1'])
    num2Input = int(request.POST['num2'] )

    # Insert into dictionary
    variables['num1'] = num1Input
    variables['num2'] = num2Input
    variables['sum']  = num1Input + num2Input

    return render(request, 'result.html', variables)


# TEST VIEW FUNCTION: actions are simply redirecting you to a url specified in cs480.proj.urls.py
def testingPage(request):
    return HttpResponse("<h1>testing page</h1>")