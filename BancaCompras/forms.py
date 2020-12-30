from django import forms
from .models import *


class UsuarioForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Código')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)


class CompraForm(forms.Form):
    tarjeta = forms.IntegerField(required=True, label='Tarjeta')
    seguridad = forms.IntegerField(required=True, label='Codigo de Seguridad')
    descripcion = forms.CharField(required=True, label='Descripcion de compra', widget=forms.Textarea)
    monto = forms.DecimalField(decimal_places=2, required=True, label='Ingrese monto', initial=0.00)
    moneda = forms.ChoiceField(choices=[('Q', 'Q'), ('$', '$')])
    fecha = forms.DateField(required=True, label='Fecha de la compra', widget=forms.DateInput)

