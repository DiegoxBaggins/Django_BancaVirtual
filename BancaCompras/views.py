from django.shortcuts import render, redirect
from .forms import *
import MySQLdb
import math
from datetime import date
from random import randint

# Create your views here.
host = 'localhost'
db_name = 'djangodic'
user = 'root'
contra = '1022'
puerto = 3306


def index(request):
    if request.method == 'POST':
        form = UsuarioForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            codigo = datos.get('usuario')
            password = datos.get('password')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo, password, tipo, estado, intentos from usuario where codigo =' + codigo + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Codigo y/o contraseña incorrectos'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'compras/index.html', dicci)
            else:
                estado = retorno[3]
                if estado == 1:
                    contradb = retorno[1]
                    if password == contradb:
                        request.session['usuario'] = codigo
                        return redirect('inicioCompras')
                    else:
                        mensaje = 'Codigo y/o contraseña incorrectos'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'compras/index.html', dicci)
                else:
                    mensaje = 'Usuario bloqueado, comuniquese con un administrador'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'compras/index.html', dicci)
        else:
            mensaje = 'Codigo y/o contraseña incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'compras/index.html', dicci)
    else:
        form = UsuarioForm()
        dicci = {'form': form}
        return render(request, 'compras/index.html', dicci)


def inicio(request):
    if request.method == 'GET':
        return render(request, 'compras/inicio.html')
    else:
        datos = request.POST
        valor = datos.get('Ingresar')
        if valor == 'Estado':
            return redirect('estadoCuenta')
        elif valor == 'Transferencia':
            return redirect('transferencias')
        elif valor == 'Terceros':
            return redirect('cuentaTerceros')
        elif valor == 'Prestamo':
            return redirect('prestamo')
        elif valor == 'Tarjeta':
            return redirect('tarjetas')
        elif valor == 'Preautorizar':
            return redirect('preautorizar')
        elif valor == 'Prestamos':
            return redirect('estadoPrestamo')