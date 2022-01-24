from django.urls import path
from . import views
'''
A path function's areguments are
    - ***string for the url***
    - a HttpRequest object (given by function in the local views.py),
    - and a name for the view to reference it as
'''
urlpatterns = [
    path('app1/', views.app1View, name='app1'),
]
