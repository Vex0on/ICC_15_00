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
            'worker': '',
            'street': 'Ulica',
            'houseNumber': 'Numer domu',
            'flatNumber': 'Numer mieszkania',
            'postcode': 'Kod pocztowy',
            'placeName': 'Miasto',
        }

        widgets = {
            'worker': forms.Select(attrs={'class': 'worker'}),
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
            'email',
            'password1',
            'password2'
        ]


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
            'client',
            'street',
            'houseNumber',
            'flatNumber',
            'postcode',
            'placeName'
        ]


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password confirmation'}))
    name = forms.CharField(max_length=45, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    surname = forms.CharField(max_length=45, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Surname'}))
    phoneNumber = forms.CharField(max_length=9, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Phone number'}))
    pesel = forms.CharField(max_length=11, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Pesel'}))
    street = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Street'}))
    houseNumber = forms.CharField(max_length=10, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'House number'}))
    flatNumber = forms.CharField(max_length=10, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Flat number'}))
    postcode = forms.CharField(max_length=6, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Postcode'}))
    placeName = forms.CharField(max_length=45, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Place name'}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        client = Client.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            phoneNumber=self.cleaned_data['phoneNumber'],
            pesel=self.cleaned_data['pesel']
        )
        client_address = ClientAddress.objects.create(
            client=client,
            street=self.cleaned_data['street'],
            houseNumber=self.cleaned_data['houseNumber'],
            flatNumber=self.cleaned_data['flatNumber'],
            postcode=self.cleaned_data['postcode'],
            placeName=self.cleaned_data['placeName']
        )

        return user
