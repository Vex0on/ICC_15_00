from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols':25}))