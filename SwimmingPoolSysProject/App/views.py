from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import allowed_users

# Create your views here.


def is_client(user):
    return user.is_authenticated and hasattr(user, 'client')


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


@user_passes_test(is_client)
def complaint(request):
    logged_user = request.user
    tickets = Ticket.objects.filter(client=logged_user)
    form_complaint = ComplaintForm(request.POST, tickets)
    if form_complaint.is_valid():
        form_complaint.save()
        return redirect('home')
    context = {
        'form_complaint': form_complaint,
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_panel(request):
    return render(request, 'App/subpages/manager/manager_panel.html')


# Manager panel list

@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_plan(request):
    return render(request, 'App/subpages/manager/manager_plan.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_panel_shift_add(request):
    form = ShiftForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('manager_panel_shift_add')
    context = {
        'form': form
    }
    return render(request, 'App/subpages/manager/manager_panel_shift_add.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_plan_list(request):
    shifts = Shift.objects.all().order_by('-startTime')
    context = {'shifts': shifts}

    if request.method == "POST":
        if request.POST.get('calendar'):
            date = request.POST.get('calendar')
            shifts = Shift.objects.filter(startTime__date=date)
            context = {
                'shifts': shifts,
                'date': date
            }
            return render(request, 'App/subpages/manager/manager_plan_list.html', context)
        return render(request, 'App/subpages/manager/manager_plan_list.html', context)
    return render(request, 'App/subpages/manager/manager_plan_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_plan_list_edit(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    form = ShiftForm(instance=shift)

    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('manager_plan_list_edit', shift_id)

    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_plan_list_edit.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_plan_list_show(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    workers = Worker.objects.filter(shift=shift)
    context = {
        'shift': shift,
        'workers': workers
    }
    return render(request, 'App/subpages/manager/manager_plan_list_show.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_plan_list_delete(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if request.method == 'POST':
        shift.delete()
        return redirect('manager_plan_list')
    return render(request, 'App/subpages/manager/manager_plan_list_delete.html', {'shift': shift})

# Manager plan employees


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees(request):
    workers = Worker.objects.all()
    context = {'workers': workers}
    return render(request, 'App/subpages/manager/manager_employees.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees_add(request):
    form = CreateWorkerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manager_employees_add_worker_address')
    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_add.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees_add_worker_address(request):
    form = CreateWorkerAddressForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manager_employees')
    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_add.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees_delete(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    if request.method == 'POST':
        worker.delete()
        return redirect('manager_employees')
    return render(request, 'App/subpages/manager/manager_employees_delete.html', {'worker': worker})


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees_show(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker_address = get_object_or_404(WorkerAddress, worker=worker)
    context = {'worker': worker,
               'workerAddress': worker_address}
    return render(request, 'App/subpages/manager/manager_employees_show.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
def manager_employees_edit(request, worker_id):
    worker = Worker.objects.get(pk=worker_id)
    form = CreateWorkerForm(instance=worker)

    if request.method == 'POST':
        form = CreateWorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('manager_employees_edit_worker_address', worker_id)

    context = {'form': form}
    return render(request, 'App/subpages/manager/manager_employees_edit.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['manager', 'admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['receptionist', 'admin'])
def receptionist_panel(request):
    return render(request, 'App/subpages/receptionist/receptionist_panel.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['receptionist', 'admin'])
def receptionist_tickets(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'App/subpages/receptionist/receptionist_tickets.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['receptionist', 'admin'])
def receptionist_tickets_add(request):
    form = CreateTicketsForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('receptionist_tickets')
    context = {'form': form}
    return render(request, 'App/subpages/receptionist/receptionist_tickets_add.html', context)


# accountant panel

@login_required(login_url='login')
@allowed_users(allowed_roles=['accountant', 'admin'])
def accountant_panel(request):
    return render(request, 'App/subpages/accountant/accountant_panel.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['accountant', 'admin'])
def accountant_accountancy(request):
    tickets = Ticket.objects.all()
    tickets_sum = round(sum([float(price.split("zł")[0])
                        for price in [ticket.price for ticket in tickets]]), 2)
    context = {'tickets': tickets, 'tickets_sum': tickets_sum}
    return render(request, 'App/subpages/accountant/accountant_accountancy.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['accountant', 'admin'])
def accountant_result(request):
    return render(request, 'App/subpages/accountant/accountant_result.html')


# Tickets


def ticket_buy_gym(request):
    return render(request, 'App/subpages/client/ticket_buy_gym.html')


def ticket_buy_spa(request):
    return render(request, 'App/subpages/client/ticket_buy_spa.html')


def ticket_buy_swimming_pool(request):
    return render(request, 'App/subpages/client/ticket_buy_swimming_pool.html')
