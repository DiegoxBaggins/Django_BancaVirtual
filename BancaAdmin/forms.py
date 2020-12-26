from django import forms
from .models import *


class UsuarioForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Código')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)


class ClienteForm(forms.Form):
    nit = forms.IntegerField(required=True, label='NIT')
    nombre = forms.CharField(required=True, label='Nombre')
    direccion = forms.CharField(required=True, label='Direccion')


class ClienteIndividualForm(ClienteForm):
    cui = forms.IntegerField(required=True, label='CUI')

    class Meta:
        fields = ('cui', 'nit', 'nombre', 'direccion')


class ClienteEmpresarialForm(ClienteForm):
    comercial = forms.CharField(required=True, label='Nombre Comercial')
    representante = forms.CharField(required=True, label='Representante Legal')
    tipo = forms.CharField(required=True, label='Tipo')

    class Meta:
        fields = ('nit', 'nombre', 'comercial', 'direccion', 'representante', 'tipo')


class CuentaForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Ingrese Codigo de Usuario', initial=0)
    monto = forms.DecimalField(decimal_places=2, required=True, label='Ingresar monto inicial a depositar', initial=0.00)
    moneda = forms.ChoiceField(choices=[('Q', 'Q'), ('$', '$')])


class CuentaMonetariaForm(CuentaForm):
    pre_cheque = forms.ChoiceField(label='Preautorizacion de Cheques', choices=[(1, 'Activado'), (0, 'Desactivado')])

    class Meta:
        fields = ('usuario', 'monto', 'moneda', 'pre_cheque')


class CuentaAhorroForm(CuentaForm):
    interes = forms.DecimalField(decimal_places=2, required=True, label='Ingresar interes de la cuenta', initial=0.00)

    class Meta:
        fields = ('usuario', 'monto', 'moneda', 'interes')


class CuentaFijoForm(CuentaAhorroForm):
    plazo = forms.CharField(required=True, label='Ingrese Plazo')
    fecha_inicio = forms.DateField(required=True, label='Ingrese Fecha de inicio', widget=forms.DateInput)

    class Meta:
        fields = ('usuario', 'monto', 'moneda', 'interes', 'plazo', 'fecha_inicio')


class ChequeraForm(forms.Form):
    cuenta = forms.IntegerField(required=True, label='Ingrese Numero de cuenta')
    
    class Meta:
        fields = 'cuenta'


class DesbloqueoForm(forms.Form):
    usuario = forms.IntegerField(required=True, label='Ingrese codigo de usuario')

    class Meta:
        fields = 'usuario'


class depositoForm(forms.Form):
    cuenta = forms.IntegerField(required=True, label='Ingrese numero de cuenta')
    monto = forms.DecimalField(decimal_places=2, required=True, label='Ingrese monto a depositar', initial=0.00)
    moneda = forms.ChoiceField(choices=[('Q', 'Q'), ('$', '$')])
    descripcion = forms.Field(required=True, label='descripcion')

    class Meta:
        fields = ('cuenta', 'monto', 'moneda', 'descripcion')


class chequeForm(forms.Form):
    cuenta = forms.IntegerField(required=True, label='Ingrese numero de cuenta')
    chequera = forms.IntegerField(required=True, label='Ingrese codigo de la chequera')
    cheque = forms.IntegerField(required=True, label='Ingrese codigo del cheque')
    monto = forms.DecimalField(decimal_places=2, required=True, label='Ingrese monto del cheque', initial=0.00)
    receptor = forms.Field(required=True, label='Nombre del receptor')

    class Meta:
        fields = ('cuenta', 'chequera', 'cheque', 'monto', 'receptor')
