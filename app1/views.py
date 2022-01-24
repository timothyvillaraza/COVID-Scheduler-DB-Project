from django.shortcuts import render
from django.http import HttpResponse

'''
Handles logic before rendering and displaying an html page
render(request, html file from folder specified in cs480proj.settings, dictionary of variables)

Dictionary of variables:
    if dictionary_of_variables = {'name' : 'tim'}
    in the html file, {{name}} will show up as 'tim'
'''

# Create your views here.
def app1View(request):
    # return HttpResponse("Hello World")

    variables = {
        'name' : 'helloWorld.html',
        'test2' : 5
    }

    return render(request, 'helloWorld.html', variables)

