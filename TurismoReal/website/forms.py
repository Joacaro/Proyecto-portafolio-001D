from django import forms

from .models import Cliente

class loginform(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=('email', 'clave')