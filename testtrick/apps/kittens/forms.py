from django import forms


class EmailKittenForm(forms.Form):
    email = forms.EmailField(required=True)
