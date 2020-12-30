from django import forms
from .models import *


class UsuarioForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Código')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)


