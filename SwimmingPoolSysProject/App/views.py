from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def homePage(request):
    return HttpResponse('<h1>Tu bedzie kozak apka xD</h1>')
