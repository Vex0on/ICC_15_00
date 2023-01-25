from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 25}))


class CreateWorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"

        labels = {
            'name': 'Imie',
            'surname': 'Nazwisko',
            'phoneNumber': 'Numer telefonu',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d', name):
            raise ValidationError('Pole nie może zawierać liczb')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if re.search(r'\d', surname):
            raise ValidationError('Pole nie może zawierać liczb')
        return surname

    def clean_phoneNumber(self):
        number = self.cleaned_data.get('phoneNumber')
        if re.search(r'[a-zA-Z]', number):
            raise forms.ValidationError("Pole nie może zawierać liter")
        if len(number) != 9:
            raise ValidationError('Numer telefonu musi zawierać 9 cyfr')
        if number[0] == '0':
            raise ValidationError('Numer nie moze sie zaczynac od 0')
        return number

    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')
        if re.search(r'[a-zA-Z]', pesel):
            raise forms.ValidationError("Pole nie może zawierać liter")
        if len(pesel) != 11:
            raise ValidationError('Pesel musi zawierać 11 cyfr')
        return pesel


class CreateWorkerAddressForm(ModelForm):
    class Meta:
        model = WorkerAddress
        fields = "__all__"

        labels = {
            'worker': 'Pracownik',
            'street': 'Ulica',
            'houseNumber': 'Numer domu',
            'flatNumber': 'Numer mieszkania',
            'postcode': 'Kod pocztowy',
            'placeName': 'Miasto',
        }

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if re.search(r'\d', street):
            raise ValidationError('Pole nie może zawierać liczb')
        return street

    def clean_placeName(self):
        place = self.cleaned_data.get('placeName')
        if re.search(r'\d', place):
            raise ValidationError('Pole nie może zawierać liczb')
        return place


class CreateTicketsForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ['price', 'zone', 'worker', 'client']
        widgets = {
            'price': forms.Select(attrs={'class': 'price'}),
            'zone': forms.Select(attrs={'class': 'zone'}),
            'worker': forms.Select(attrs={'class': 'worker'}),
            'client': forms.Select(attrs={'class': 'client'})
        }


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = "__all__"
        labels = {
            'worker': 'Pracownicy',
            'startTime': 'Początek zmiany',
            'description': 'Zmiana'
        }
        widgets = {
            'startTime': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'startTime'
                }
            ),
        }

    def clean_startTime(self):
        startTime = self.cleaned_data.get('startTime')
        today = datetime.datetime.now()
        if startTime.replace(tzinfo=None) < today:
            raise ValidationError('Data nie może być z przeszłości')
        return startTime


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.EmailInput()
        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'surname',
            'phoneNumber',
            'email',
            'pesel'
        ]


class ClientAddressForm(ModelForm):
    class Meta:
        model = ClientAddress
        fields = [
            'street',
            'houseNumber',
            'flatNumber',
            'postcode',
            'placeName'
        ]


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'


class BuyTicketFormSPA(ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'price', 'zone']

        widgets = {
            'client': forms.HiddenInput(),
            'price': forms.Select(attrs={'class': 'price'}),
            'zone': forms.Select(attrs={'class': 'zone'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            try:
                self.fields['client'].initial = Client.objects.get(user=user)
            except Client.DoesNotExist:
                pass
        self.fields['zone'].choices = [("SPA", "SPA")]


class BuyTicketFormGym(ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'price', 'zone']

        widgets = {
            'client': forms.HiddenInput(),
            'price': forms.Select(attrs={'class': 'price'}),
            'zone': forms.Select(attrs={'class': 'zone'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            try:
                self.fields['client'].initial = Client.objects.get(user=user)
            except Client.DoesNotExist:
                pass
        self.fields['zone'].choices = [("Siłownia", "Siłownia")]


class BuyTicketFormSwimmingPool(ModelForm):
    class Meta:
        model = Ticket
        fields = ['client', 'price', 'zone']

        widgets = {
            'client': forms.HiddenInput(),
            'price': forms.Select(attrs={'class': 'price'}),
            'zone': forms.Select(attrs={'class': 'zone'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            try:
                self.fields['client'].initial = Client.objects.get(user=user)
            except Client.DoesNotExist:
                pass
        self.fields['zone'].choices = [("Pływalnia", "Pływalnia")]
