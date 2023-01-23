from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import *

# Create your views here.


def homePage(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            html = render_to_string('App/contact_form.html', {
                'name': name,
                'email': email,
                'message': message
            })

            send_mail('Formularz kontaktowy', 'wiadomosc', 'pocalunekneptuna@gmail.com', ['pocalunekneptuna@gmail.com'],
                      html_message=html)
            messages.info(request, 'Successfully Sent The Message!')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'App/index.html', context)


# login

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Nazwa użytkownika jest niepoprawna')
            return render(request, 'App/subpages/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Hasło nie jest zgodne.')
            return render(request, 'App/subpages/login.html')

    return render(request, 'App/subpages/login.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


def registration(request):
    return render(request, 'App/subpages/registration.html')


def remind_password(request):
    return render(request, 'App/subpages/remind_password.html')


# Manager panel

def manager_panel(request):
    return render(request, 'App/subpages/manager/manager_panel.html')


# Manager panel list


def manager_plan(request):
    return render(request, 'App/subpages/manager/manager_plan.html')


def manager_plan_list(request):
    return render(request, 'App/subpages/manager/manager_plan_list.html')
    #     if request.POST.get('calendar'):
    #         date = request.POST.get('calendar')
    #         shifts = Shift.objects.filter(startTime__date=date)
    #         context = {'shifts': shifts}
    #         return render(request, 'App/subpages/manager/manager_plan_list.html', context)
    #     else:
    #         return render(request, 'App/subpages/manager/manager_plan.html')
            

# Manager plan employees


def manager_employees(request):
    workers = Worker.objects.all()
    context = {'workers': workers}
    return render(request, 'App/subpages/manager/manager_employees.html', context)


def manager_employees_add(request):
    return render(request, 'App/subpages/manager/manager_employees_add.html')


def manager_employees_show(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    workerAddress = get_object_or_404(WorkerAddress, worker=worker)
    context = {'worker': worker,
               'workerAddress': workerAddress}
    return render(request, 'App/subpages/manager/manager_employees_show.html', context)


def manager_employees_delete(request):
    return render(request, 'App/subpages/manager/manager_employees_delete.html')
