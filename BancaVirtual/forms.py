from django import forms
from .models import *


class UsuarioForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Código')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)


class AgregarUsuarioForm(forms.Form):
    cuenta = forms.IntegerField(required=True, label='Ingrese Numero de cuenta')
    nombre = forms.CharField(required=True, label='Nombre')

    class Meta:
        fields = 'cuenta'


class TransferenciasPropiasForm(forms.Form):

    def __init__(self, lista):
        super(TransferenciasPropiasForm, self).__init__()
        self.fields['cuentas'] = forms.ChoiceField(choices=tuple([(codigo, codigo) for codigo in lista]))

    class Meta:
        fields = 'cuentas'


class chequeForm(forms.Form):
    cuenta = forms.IntegerField(required=True, label='Ingrese numero de cuenta')
    chequera = forms.IntegerField(required=True, label='Ingrese codigo de la chequera')
    cheque = forms.IntegerField(required=True, label='Ingrese codigo del cheque')
    monto = forms.DecimalField(decimal_places=2, required=True, label='Ingrese monto del cheque', initial=0.00)
    receptor = forms.Field(required=True, label='Nombre del receptor')

    class Meta:
        fields = ('cuenta', 'chequera', 'cheque', 'monto', 'receptor')
