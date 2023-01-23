from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
import re


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 25}))


class CreateWorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"

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



