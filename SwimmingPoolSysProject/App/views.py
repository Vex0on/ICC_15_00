from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages

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

            send_mail('Formularz kontaktowy', 'wiadomosc', 'pocalunekneptuna@gmail.com', ['pocalunekneptuna@gmail.com'], html_message=html)
            messages.info(request, 'Successfully Sent The Message!')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'App/index.html', context)


def login(request):
    return render(request, 'App/subpages/login.html')


def registration(request):
    return render(request, 'App/subpages/registration.html')


def remind_password(request):
    return render(request, 'App/subpages/remind_password.html')
