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
        form = CompraForm()
        dicci = {'form': form}
        return render(request, 'compras/inicio.html', dicci)
    else:
        form = CompraForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            tarjeta = datos.get('tarjeta')
            seguridad = datos.get('seguridad')
            monto = datos.get('monto')
            moneda = datos.get('moneda')
            descripcion = datos.get('descripcion')
            fecha = datos.get('fecha')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select * from tcredito where numero = ' + str(tarjeta) + " and seguridad = "+ str(seguridad)  + " ;"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Tarjeta Inexistente o codigo de seguridad incorrecto'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'compras/inicio.html', dicci)
            else:
                limite = retorno[2]
                gasto = retorno[3]
                marca = retorno[4]
                bono = retorno[6]
                gasto_permitido = float(limite) - float(gasto)
                puntos = calcularPuntos(float(monto), marca, moneda)
                if float(puntos[1]) > gasto_permitido:
                    mensaje = 'El gasto actual ya no permite la compra, supera el limite de la tarjeta'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'compras/inicio.html', dicci)
                else:
                    nuevo_gasto = float(gasto) + float(puntos[1])
                    nuevo_bono = float(bono) + puntos[0]
                    cosulta = "update tcredito set gasto = " + str(nuevo_gasto) + " where numero = " + str(tarjeta) + ";"
                    c.execute(cosulta)
                    db.commit()
                    cosulta = "update tcredito set bono = " + str(nuevo_bono) + " where numero = " + str(tarjeta) + ";"
                    c.execute(cosulta)
                    db.commit()
                    cosulta = "insert into transtarjeta (monto,fecha,descripcion,tipo,porcentaje,tarjeta) values " \
                              "(" + str(monto) + ",'" + str(fecha) + "','" + str(descripcion) + "','" + moneda + "'," \
                              " 1," + str(tarjeta) + ");"
                    c.execute(cosulta)
                    db.commit()
                    if marca == 'prefepuntos':
                        cosulta = "insert into transtarjeta (monto,fecha,descripcion,tipo,porcentaje,tarjeta) values " \
                                  "(" + str(puntos[0]) + ",'" + str(fecha) + "','" + str(
                            descripcion) + "','puntos',1," + str(tarjeta) + ");"
                        c.execute(cosulta)
                        db.commit()
                    else:
                        cosulta = "insert into transtarjeta (monto,fecha,descripcion,tipo,porcentaje,tarjeta) values " \
                                  "(" + str(puntos[0]) + ",'" + str(fecha) + "','" + str(descripcion) + "','cashback',1," + str(tarjeta) + ");"
                        c.execute(cosulta)
                        db.commit()
                    mensaje = 'Compra registrada con exito'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'compras/inicio.html', dicci)


def calcularPuntos(monto, marca, moneda):
    if marca == 'prefepuntos':
        if moneda == '$':
            monto = monto * 7.63
        if monto <= 100.00:
            puntos = 0
            return puntos, monto
        elif 100.00 < monto <= 500.00:
            puntos = monto * 0.02
            return puntos, monto
        elif 500.00 < monto <= 2000.00:
            puntos = monto * 0.04
            return puntos, monto
        elif monto > 2000.00:
            puntos = monto * 0.05
            return puntos, monto
    elif marca == 'cashback':
        if moneda == '$':
            monto = monto * 7.87
        if monto <= 200.00:
            puntos = 0
            return puntos, monto
        elif 200.00 < monto <= 700.00:
            puntos = monto * 0.02
            return puntos, monto
        elif monto > 700.00:
            puntos = monto * 0.05
            return puntos, monto
