from django import forms
from django.forms import ModelForm
from .models import *


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 25}))


class CreateWorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"
