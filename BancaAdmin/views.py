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
            cosulta = 'select codigo, password, tipo from usuario where codigo =' + codigo + " and password ='" \
                      + password + "';"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Codigo y/o contraseña incorrectos'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'index.html', dicci)
            else:
                contradb = retorno[1]
                tipo = retorno[2]
                if password == contradb:
                    if tipo == 0:
                        return redirect('inicio')
                    else:
                        mensaje = 'Esta plataforma es unicamente para administradores'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'index.html', dicci)
                else:
                    mensaje = 'Codigo y/o contraseña incorrectos'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'index.html', dicci)
        else:
            mensaje = 'Codigo y/o contraseña incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'index.html', dicci)
    else:
        form = UsuarioForm()
        dicci = {'form': form}
        return render(request, 'index.html', dicci)


def inicio(request):
    if request.method == 'GET':
        return render(request, 'admins/inicioAdmin.html')
    else:
        datos = request.POST
        valor = datos.get('Ingresar')
        if valor == 'Nuevo':
            return redirect('nuevoCliente')
        elif valor == 'Cuenta':
            return redirect('nuevaCuenta')
        elif valor == 'Chequera':
            return redirect('nuevaChequera')
        elif valor == 'Desbloquear':
            return redirect('desbloqueo')
        elif valor == 'Deposito':
            return redirect('deposito')
        elif valor == 'Cheque':
            return redirect('cambioCheque')


def nuevoCliente(request):
    if request.method == 'GET':
        return render(request, 'admins/nuevoCliente.html')
    else:
        datos = request.POST
        valor = datos.get('Ingresar')
        if valor == 'Individual':
            return redirect('nuevoIndividual')
        elif valor == 'Empresarial':
            return redirect('nuevoEmpresarial')


def nuevoIndividual(request):
    if request.method == 'GET':
        form = ClienteIndividualForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevoIndividual.html', dicci)
    else:
        form = ClienteIndividualForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cui = datos.get('cui')
            nit = datos.get('nit')
            nombre = datos.get('nombre')
            direccion = datos.get('direccion')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select cui from c_individual where cui =' + cui + ';'
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is not None:
                mensaje = 'Cliente ya registrado'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevoIndividual.html', dicci)
            else:
                usuario = randint(100000, 999999)
                contra_nueva = randint(1000, 9999)
                consulta = 'insert into usuario values (' + str(usuario) + ",'" + str(contra_nueva) + "'," + str(1) + ',1,0);'
                c.execute(consulta)
                db.commit()
                consulta = 'insert into c_individual values (' + cui + ',' + nit + ",'" + nombre \
                           + "','" + direccion + "'," + str(usuario) + ');'
                c.execute(consulta)
                db.commit()
                c.close()
                mensaje = 'Cliente Registrado correctamente'
                dicci = {'form': form, 'mensaje': mensaje, 'usuario': 'usuario:' + str(usuario),
                 'contra': 'contraseña: ' + str(contra_nueva)}
                return render(request, 'admins/nuevoIndividual.html',dicci)
        else:
            mensaje = 'Datos incompletos o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevoIndividual.html', dicci)


def nuevoEmpresarial(request):
    if request.method == 'GET':
        form = ClienteEmpresarialForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevoEmpresarial.html', dicci)
    else:
        form = ClienteEmpresarialForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            nit = datos.get('nit')
            nombre = datos.get('nombre')
            comercial = datos.get('comercial')
            representante = datos.get('representante')
            direccion = datos.get('direccion')
            tipo = datos.get('tipo')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select nit from c_empresarial where nit =' + nit + ';'
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is not None:
                mensaje = 'Cliente ya registrado'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevoEmpresarial.html', dicci)
            else:
                usuario = randint(100000, 999999)
                contra_nueva = randint(1000, 9999)
                consulta = 'insert into usuario values (' + str(usuario) + ",'" + str(contra_nueva) + "'," + str(2) + ',1,0);'
                c.execute(consulta)
                db.commit()
                abreviacion = registrarTipoE(tipo)
                consulta = 'insert into c_empresarial values (' + nit + ",'" + nombre + "','" + comercial \
                           + "','" + representante + "','" + direccion + "'," + str(usuario) + ",'" + abreviacion + "');"
                c.execute(consulta)
                db.commit()
                c.close()
                mensaje = 'Cliente Registrado correctamente'
                dicci = {'form': form, 'mensaje': mensaje, 'usuario': 'usuario:' +
                        str(usuario), 'contra': 'contraseña: ' + str(contra_nueva)}
                return render(request, 'admins/nuevoIndividual.html', dicci)
        else:
            mensaje = 'Datos incompletos o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevoIndividual.html', dicci)


def registrarTipoE(tipo):
    lista1 = list(tipo)
    abre = lista1[0] + lista1[1] + lista1[2]
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select abreviacion from tipo_empresa where abreviacion = '" + abre + "';"
    c.execute(cosulta)
    retorno = c.fetchone()
    if retorno is not None:
        return abre
    else:
        consulta = "insert into tipo_empresa values ('" + abre + "','" + tipo + "');"
        c.execute(consulta)
        db.commit()
        c.close()
        return abre


def nuevaCuenta(request):
    if request.method == 'GET':
        return render(request, 'admins/nuevaCuenta.html')
    else:
        datos = request.POST
        valor = datos.get('Ingresar')
        if valor == 'Monetaria':
            return redirect('nuevaMonetaria')
        elif valor == 'Ahorro':
            return redirect('nuevaAhorro')
        else:
            return redirect('nuevaPlazo')


def nuevaMonetaria(request):
    if request.method == 'GET':
        form = CuentaMonetariaForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevaMonetaria.html', dicci)
    else:
        form = CuentaMonetariaForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            usuario = datos.get('usuario')
            monto = datos.get('monto')
            moneda = datos.get('moneda')
            pre_cheque = datos.get('pre_cheque')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo from usuario where codigo =' + usuario + ';'
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cliente no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaMonetaria.html', dicci)
            else:
                consulta = "insert into cuenta (tipo, monto, estado, moneda, pre_cheques, usuario) " \
                          "values ('monetaria',"+monto + ",1,'" + moneda + "'," + pre_cheque + "," + usuario + ");"
                c.execute(consulta)
                db.commit()
                consulta = 'select codigo from cuenta order by codigo desc limit 1;'
                c.execute(consulta)
                retorno = c.fetchone()
                codigo_cuenta = retorno[0]
                c.close()
                mensaje = 'Cuenta registrada con exito. \n cuenta numero: ' + str(codigo_cuenta)
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaMonetaria.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevaMonetaria.html', dicci)


def nuevaAhorro(request):
    if request.method == 'GET':
        form = CuentaAhorroForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevaAhorro.html', dicci)
    else:
        form = CuentaAhorroForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            usuario = datos.get('usuario')
            monto = datos.get('monto')
            moneda = datos.get('moneda')
            interes = datos.get('interes')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo from usuario where codigo =' + usuario + ';'
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cliente no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaAhorro.html', dicci)
            else:
                consulta = "insert into cuenta (tipo, monto, estado, moneda, pre_cheques,interes, usuario) " \
                           "values ('ahorro'," + monto + ",1,'" + moneda + "', 0," + interes + "," + usuario + ");"
                c.execute(consulta)
                db.commit()
                consulta = 'select codigo from cuenta order by codigo desc limit 1;'
                c.execute(consulta)
                retorno = c.fetchone()
                codigo_cuenta = retorno[0]
                c.close()
                mensaje = 'Cuenta registrada con exito. \n cuenta numero: ' + str(codigo_cuenta)
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaAhorro.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevaAhorro.html', dicci)


def nuevaPlazo(request):
    if request.method == 'GET':
        form = CuentaFijoForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevaPlazoFijo.html', dicci)
    else:
        form = CuentaFijoForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            usuario = datos.get('usuario')
            monto = datos.get('monto')
            moneda = datos.get('moneda')
            interes = datos.get('interes')
            plazo = datos.get('plazo')
            fecha = datos.get('fecha_inicio')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo from usuario where codigo =' + usuario + ';'
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cliente no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaPlazoFijo.html', dicci)
            else:
                consulta = "insert into cuenta (tipo, monto, estado, moneda, pre_cheques, interes, plazo, " \
                           "fecha_inicio, usuario) values ('plazo fijo'," + monto + ",1,'" + moneda + "', 0," + interes\
                           + ",'" + plazo + "','" + fecha + "'," + usuario + ");"
                c.execute(consulta)
                db.commit()
                consulta = 'select codigo from cuenta order by codigo desc limit 1;'
                c.execute(consulta)
                retorno = c.fetchone()
                codigo_cuenta = retorno[0]
                c.close()
                mensaje = 'Cuenta registrada con exito. \n cuenta numero: ' + str(codigo_cuenta)
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaPlazoFijo.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevaPlazoFijo.html', dicci)


def nuevaChequera(request):
    if request.method == 'GET':
        form = ChequeraForm()
        dicci = {'form': form}
        return render(request, 'admins/nuevaChequera.html', dicci)
    else:
        form = ChequeraForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cuenta = datos.get('cuenta')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo from cuenta where codigo =' + cuenta + " and tipo = 'monetaria';"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cuenta no existe o no es monetaria'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/nuevaChequera.html', dicci)
            else:
                cosulta = 'select codigo from chequera where cuenta =' + cuenta + " and cantidad > 0;"
                c.execute(cosulta)
                retorno = c.fetchone()
                if retorno is not None:
                    mensaje = 'Cuenta ya cuenta con una chequera activa'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/nuevaChequera.html', dicci)
                else:
                    consulta = "insert into chequera (cantidad, cuenta) values (10," + cuenta + ");"
                    c.execute(consulta)
                    db.commit()
                    consulta = 'select codigo from chequera order by codigo desc limit 1;'
                    c.execute(consulta)
                    retorno = c.fetchone()
                    chequera = retorno[0]
                    cheques = 1
                    while cheques <= 10:
                        consulta = 'insert into cheque values (' + str(cheques) + ',' + str(chequera) + ',' + "'generado');"
                        c.execute(consulta)
                        db.commit()
                        cheques += 1
                    c.close()
                    mensaje = 'Chequera Registrada con exito \nCodigo chequera: ' + str(chequera)
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/nuevaChequera.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/nuevaChequera.html', dicci)


def desbloqueo(request):
    if request.method == 'GET':
        form = DesbloqueoForm()
        dicci = {'form': form}
        return render(request, 'admins/desbloqueo.html', dicci)
    else:
        form = DesbloqueoForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            usuario = datos.get('usuario')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo from usuario where codigo = ' + usuario + " ;"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cuenta no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/desbloqueo.html', dicci)
            else:
                cosulta = 'select estado from usuario where codigo  = ' + usuario + " ;"
                c.execute(cosulta)
                retorno = c.fetchone()
                estado = retorno[0]
                if estado == 1:
                    mensaje = 'Cuenta esta activada'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/desbloqueo.html', dicci)
                else:
                    consulta = "update usuario set estado = 1 where codigo = " + usuario + ";"
                    c.execute(consulta)
                    db.commit()
                    cosulta = 'update usuario set intentos = 0 where codigo = ' + usuario + ';'
                    c.execute(cosulta)
                    db.commit()
                    c.close()
                    mensaje = 'Usuario Desbloqueado con exito'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/desbloqueo.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/desbloqueo.html', dicci)


def deposito(request):
    if request.method == 'GET':
        form = depositoForm()
        dicci = {'form': form}
        return render(request, 'admins/deposito.html', dicci)
    else:
        form = depositoForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cuenta = datos.get('cuenta')
            monto = datos.get('monto')
            moneda = datos.get('moneda')
            descripcion = datos.get('descripcion')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select * from cuenta where codigo = ' + cuenta + " ;"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cuenta Inexistente'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/deposito.html', dicci)
            else:
                if retorno[3] == 1:
                    dinero = float(retorno[2])
                    monedaC = retorno[4]
                    agregar = conversionMoneda(monedaC, moneda, float(monto))
                    dinero += float(agregar)
                    consulta = "update cuenta set monto = " + str(dinero) + " where codigo = " + cuenta + ";"
                    c.execute(consulta)
                    db.commit()
                    consulta = "insert into transaccion (monto, fecha, descripcion, tipo, cuenta) values (" +\
                               str(agregar) + ",'" + str(date.today()) + "','"+ descripcion + "','deposito'," + cuenta + ');'
                    c.execute(consulta)
                    db.commit()
                    c.close()
                    mensaje = 'Deposito Realizado con exito'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/deposito.html', dicci)
                else:
                    mensaje = 'La cuenta se encuentra bloqueada, no se permiten los depositos'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/deposito.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/deposito.html', dicci)


def conversionMoneda(cuenta, depositar, monto):
    if cuenta == depositar:
        return monto
    if cuenta == 'Q':
        nuevo = monto * 7.60
        return nuevo
    else:
        nuevo = monto / 7.87
        return nuevo


def cambioCheque(request):
    if request.method == 'GET':
        form = chequeForm()
        dicci = {'form': form}
        return render(request, 'admins/cambioCheque.html', dicci)
    else:
        form = chequeForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cuenta = datos.get('cuenta')
            chequera = datos.get('chequera')
            monto = datos.get('monto')
            cheque = datos.get('cheque')
            receptor = datos.get('receptor')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = "select cuenta.monto, cuenta.pre_cheques, chequera.cantidad, cheque.estado, cuenta.estado from cuenta, chequera," \
                      " cheque where cuenta.codigo=chequera.cuenta and cheque.chequera=chequera.codigo " \
                      "and cuenta.codigo = " + cuenta + " and chequera.codigo = "+ chequera + " and " \
                      "cheque.codigo = " + cheque + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Datos incorrectos, cuenta, chequera o cheque inexistente'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'admins/cambioCheque.html', dicci)
            else:
                monto_cuenta = retorno[0]
                preautorizacion = retorno[1]
                cantidad_cheques = retorno[2]
                estado_cheque = retorno[3]
                estado_cuenta = retorno[4]
                if estado_cuenta == 1:
                    if estado_cheque != 'generado':
                        mensaje = 'Cheque ya ha sido cambiado'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'admins/cambioCheque.html', dicci)
                    else:
                        if float(monto) > float(monto_cuenta):
                            mensaje = 'Monto no disponible en la cuenta'
                            dicci = {'form': form, 'mensaje': mensaje}
                            return render(request, 'admins/cambioCheque.html', dicci)
                        else:
                            if preautorizacion == 0:
                                dinero = float(monto_cuenta) - float(monto)
                                consulta = "update cuenta set monto = " + str(dinero) + " where codigo = " + cuenta + ";"
                                c.execute(consulta)
                                db.commit()
                                consulta = "insert into transaccion (monto, fecha, descripcion, tipo, cuenta) values (" + \
                                           str(monto) + ",'" + str(date.today()) + "','cambio de cheque preautorizado " \
                                           "por " + receptor + "','retiro'," + cuenta + ');'
                                c.execute(consulta)
                                db.commit()
                                cantidad = cantidad_cheques - 1
                                consulta = "update chequera set cantidad = " + str(cantidad) + " where codigo =" \
                                           + chequera + ";"
                                c.execute(consulta)
                                db.commit()
                                consulta = "update cheque set estado = 'cobrado' where codigo =" + cheque + \
                                           " and chequera = " + chequera + ";"
                                c.execute(consulta)
                                db.commit()
                                c.close()
                                mensaje = 'Cambio de Cheque Realizado con exito con exito'
                                dicci = {'form': form, 'mensaje': mensaje}
                                return render(request, 'admins/cambioCheque.html', dicci)
                            else:
                                cosulta = "select * from precheque where codigo = " + cheque + " and chequera = " + \
                                          chequera + " and estado ='emitido' ;"
                                c.execute(cosulta)
                                retorno = c.fetchone()
                                if retorno is None:
                                    mensaje = 'La cuenta tiene activado la preautorizacion de cheques \n' \
                                              'Este cheque no ha sido preautorizado o esta bloqueado'
                                    dicci = {'form': form, 'mensaje': mensaje}
                                    return render(request, 'admins/cambioCheque.html', dicci)
                                else:
                                    monto_pre = str(retorno[3])
                                    destinatario_pre = retorno[4]
                                    if monto != monto_pre or receptor != destinatario_pre:
                                        consulta = "update precheque set estado = 'bloqueado' where codigo = " + cheque \
                                                   + " and chequera = " + chequera + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        cantidad = cantidad_cheques - 1
                                        consulta = "update chequera set cantidad = " + str(cantidad) + " where codigo =" \
                                                   + chequera + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        mensaje = 'La cuenta tiene activado la preautorizacion de cheques \n' \
                                                  'Los datos del cheque no coinciden \n Cheque bloqueado'
                                        dicci = {'form': form, 'mensaje': mensaje}
                                        return render(request, 'admins/cambioCheque.html', dicci)
                                    else:
                                        consulta = "update precheque set estado = 'cobrado' where codigo = " + cheque \
                                                   + " and chequera = " + chequera + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        dinero = float(monto_cuenta) - float(monto)
                                        consulta = "update cuenta set monto = " + str(dinero) + " where codigo = " + cuenta + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        consulta = "insert into transaccion (monto, fecha, descripcion, tipo, cuenta) " \
                                                   "values (" + str(monto) + ",'" + str(date.today()) + \
                                                   "','cambio de cheque preautorizado por " + receptor + "','retiro'," \
                                                   + cuenta + ');'
                                        c.execute(consulta)
                                        db.commit()
                                        cantidad = cantidad_cheques - 1
                                        consulta = "update chequera set cantidad = " + str(cantidad) + " where codigo =" \
                                                   + chequera + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        consulta = "update cheque set estado = 'cobrado' where codigo =" + cheque +\
                                                   " and chequera = " + chequera + ";"
                                        c.execute(consulta)
                                        db.commit()
                                        c.close()
                                        mensaje = 'Cambio de Cheque Realizado con exito con exito'
                                        dicci = {'form': form, 'mensaje': mensaje}
                                        return render(request, 'admins/cambioCheque.html', dicci)
                else:
                    mensaje = 'La cuenta esta bloqueada, no se puede hacer transaccion de ningun tipo'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'admins/cambioCheque.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'admins/cambioCheque.html', dicci)
