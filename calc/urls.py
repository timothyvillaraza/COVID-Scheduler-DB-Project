from django.contrib import admin
from django.urls import path, include
from . import views

'''
[Copied description from app1.url]
A path function's areguments are
    - string for the url,
    - a HttpRequest object (given by function in the local views.py),
    - and a name for the view to reference it as
'''
urlpatterns = [
        path('', views.calcView, name='calc1'),
        path('myAddPage/', views.add, name='add'),
        path('testingPage/', views.testingPage),
]
