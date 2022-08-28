from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    text = forms.CharField(max_length=1000, required=True)
