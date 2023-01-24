from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import *
from .forms import *

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

def regulations(request):
    return render(request, 'App/subpages/regulations.html')


# Manager panel

def manager_panel(request):
    return render(request, 'App/subpages/manager/manager_panel.html')


# Manager panel list


def manager_plan(request):
    return render(request, 'App/subpages/manager/manager_plan.html')


def manager_plan_list(request):
    workers = Worker.objects.all()
    context = {'workers': workers}
    return render(request, 'App/subpages/manager/manager_plan_list.html', context)


# Manager plan employees


def manager_employees(request):
    workers = Worker.objects.all()
    context = {'workers': workers}
    return render(request, 'App/subpages/manager/manager_employees.html', context)


def manager_employees_add(request):
    form = CreateWorkerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manager_employees_add_worker_address')
    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_add.html', context)


def manager_employees_add_worker_address(request):
    form = CreateWorkerAddressForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manager_employees')
    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_add.html', context)


def manager_employees_delete(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    if request.method == 'POST':
        worker.delete()
        return redirect('manager_employees')
    return render(request, 'App/subpages/manager/manager_employees_delete.html', {'worker': worker})


def manager_employees_show(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker_address = get_object_or_404(WorkerAddress, worker=worker)
    context = {'worker': worker,
               'workerAddress': worker_address}
    return render(request, 'App/subpages/manager/manager_employees_show.html', context)


def manager_employees_edit(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    form = CreateWorkerForm(instance=worker)

    if request.method == 'POST':
        form = CreateWorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('manager_employees_edit_worker_address', worker_id)

    context = {'form':form}
    return render(request, 'App/subpages/manager/manager_employees_edit.html', context)


def manager_employees_edit_worker_address(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    worker_address = WorkerAddress.objects.get(worker=worker)
    form = CreateWorkerAddressForm(instance=worker_address)

    if request.method == 'POST':
        form = CreateWorkerAddressForm(request.POST, instance=worker_address)
        if form.is_valid():
            form.save()
            return redirect('manager_employees')

    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_edit.html', context)


# receptionist panel


def receptionist_panel(request):
    return render(request, 'App/subpages/receptionist/receptionist_panel.html')


def receptionist_tickets(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'App/subpages/receptionist/receptionist_tickets.html', context)


def receptionist_tickets_add(request):
    form = CreateTicketsForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('receptionist_tickets')
    context = {'form': form}
    return render(request, 'App/subpages/receptionist/receptionist_tickets_add.html', context)


# accountant panel


def accountant_panel(request):
    return render(request, 'App/subpages/accountant/accountant_panel.html')


def accountant_accountancy(request):
    return render(request, 'App/subpages/accountant/accountant_accountancy.html')


def accountant_result(request):
    return render(request, 'App/subpages/accountant/accountant_result.html')


# Tickets


def ticket_buy_gym(request):
    return render(request, 'App/subpages/client/ticket_buy_gym.html')


def ticket_buy_spa(request):
    return render(request, 'App/subpages/client/ticket_buy_spa.html')


def ticket_buy_swimming_pool(request):
    return render(request, 'App/subpages/client/ticket_buy_swimming_pool.html')
