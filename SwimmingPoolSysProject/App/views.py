from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def homePage(request):
    return render(request, 'App/index.html')


def login(request):
    return render(request, 'App/subpages/login.html')


def registration(request):
    return render(request, 'App/subpages/registration.html')


def remind_password(request):
    return render(request, 'App/subpages/remind_password.html')
