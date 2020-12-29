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
                return render(request, 'index.html', dicci)
            else:
                estado = retorno[3]
                if estado == 1:
                    contradb = retorno[1]
                    if password == contradb:
                        cosulta = 'update usuario set intentos = 0 where codigo = ' + codigo + ';'
                        c.execute(cosulta)
                        db.commit()
                        tipo = retorno[2]
                        if tipo == 1:
                            request.session['usuario'] = codigo
                            return redirect('estadoCuenta')
                        elif tipo == 2:
                            request.session['usuario'] = codigo
                            return redirect('estadoCuentaEm')
                        else:
                            mensaje = 'Esta no es la plataforma de administrador'
                            dicci = {'form': form, 'mensaje': mensaje}
                            return render(request, 'index.html', dicci)
                    else:
                        intentos = retorno[4]
                        intentos += 1
                        print(intentos)
                        if intentos >= 3:
                            cosulta = 'update usuario set estado = 0 where codigo = ' + codigo + ';'
                            c.execute(cosulta)
                            db.commit()
                            mensaje = 'Intentos superados, usuario bloqueado'
                            dicci = {'form': form, 'mensaje': mensaje}
                            return render(request, 'index.html', dicci)
                        cosulta = 'update usuario set intentos = ' + str(intentos) + ' where codigo = ' + codigo + ';'
                        c.execute(cosulta)
                        db.commit()
                        mensaje = 'Codigo y/o contraseña incorrectos'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'index.html', dicci)
                else:
                    mensaje = 'Usuario bloqueado, comuniquese con un administrador'
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
        return render(request, 'inicio.html')
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


def inicioEm(request):
    if request.method == 'GET':
        return render(request, 'empresarial/inicioEmpresarial.html')
    else:
        datos = request.POST
        valor = datos.get('Ingresar')
        if valor == 'Estado':
            return redirect('estadoCuentaEm')
        elif valor == 'Transferencia':
            return redirect('transferenciasEm')
        elif valor == 'Terceros':
            return redirect('cuentaTercerosEm')
        elif valor == 'Prestamo':
            return redirect('prestamo')
        elif valor == 'Servicios':
            return redirect('pagos')
        elif valor == 'Preautorizar':
            return redirect('preautorizarEm')
        elif valor == 'Planilla':
            return redirect('planillas')
        elif valor == 'Proveedor':
            return redirect('proveedores')


def estadoC(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from c_individual inner join usuario on c_individual.usuario = usuario.codigo where usuario ="+ usuario + ";"
    c.execute(cosulta)
    retorno = c.fetchone()
    nombre = retorno[2]
    cui = str(retorno[0])
    nit = str(retorno[1])
    direccion = retorno[3]
    if request.method == 'GET':
        cosulta = "select cuenta.codigo, cuenta.tipo, c_individual.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                  "from c_individual, usuario, cuenta where c_individual.usuario = usuario.codigo and " \
                  "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + ";"
        c.execute(cosulta)
        retorno = c.fetchall()
        lista = ConvertirTupla(retorno)
        mensaje = 'Cuentas'
        dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
        return render(request, 'estadoCuenta.html', dicci)
    else:
        datos = request.POST
        filtro = datos.get('Ingresar')
        bloqueo = datos.get('Bloqueo')
        histo = datos.get('Historial')
        if filtro is not None:
            if filtro == 'Monetaria':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_individual.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_individual, usuario, cuenta where c_individual.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'monetaria' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas Monetarias'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
                return render(request, 'estadoCuenta.html', dicci)
            elif filtro == 'Ahorro':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_individual.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_individual, usuario, cuenta where c_individual.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'ahorro' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas de ahorro'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
                return render(request, 'estadoCuenta.html', dicci)
            elif filtro == 'Plazo':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_individual.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_individual, usuario, cuenta where c_individual.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'plazo fijo' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas Plazo Fijo'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
                return render(request, 'estadoCuenta.html', dicci)
        elif bloqueo is not None:
            cosulta = "select estado from cuenta where codigo = " + bloqueo + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            print(retorno)
            if retorno[0] == 1:
                consulta = 'update cuenta set estado = 0 where codigo = ' + bloqueo + ';'
                print(consulta)
                c.execute(consulta)
                db.commit()
                c.close()
            else:
                consulta = 'update cuenta set estado = 1 where codigo = ' + bloqueo + ';'
                c.execute(consulta)
                db.commit()
                c.close()
            return redirect('estadoCuenta')
        elif histo is not None:
            cosulta = "select moneda from cuenta where codigo = " + histo + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            request.session['cuenta'] = histo
            request.session['moneda'] = retorno[0]
            return redirect('historial')


def ConvertirTupla(retorno):
    lista = []
    for tupla in retorno:
        lista.append(list(tupla))
    for elementos in lista:
        if elementos[5] == 1:
            elementos[5] = 'Activa'
            elementos.append('Bloquear')
        else:
            elementos[5] = 'Bloqueada'
            elementos.append('Activar')
    return lista


def historial(request):
    usuario = str(request.session['usuario'])
    cuenta = str(request.session['cuenta'])
    moneda = request.session['moneda']
    print(cuenta)
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from transaccion where cuenta =" + cuenta + ";"
    c.execute(cosulta)
    retorno = c.fetchall()
    mensaje = cuenta
    dicci = {'cuentas': retorno, 'titulo': mensaje, 'moneda': moneda}
    return render(request, 'historial.html', dicci)


def nuevaC(request):
    usuario = str(request.session['usuario'])
    if request.method == 'GET':
        form = AgregarUsuarioForm()
        dicci = {'form': form}
        return render(request, 'registrarCuenta.html', dicci)
    else:
        form = AgregarUsuarioForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cuenta = datos.get('cuenta')
            nombre = datos.get('nombre')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo, usuario from cuenta where codigo =' + cuenta + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cuenta no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'registrarCuenta.html', dicci)
            else:
                terceros = str(retorno[0])
                usuario_cuenta = str(retorno[1])
                if usuario != usuario_cuenta:
                    cosulta = "select * from cuenta_tercero where usuario = " + usuario + " and cuenta = " + terceros + ";"
                    c.execute(cosulta)
                    retorno = c.fetchone()
                    if retorno is None:
                        cosulta = "insert into cuenta_tercero values(" + usuario + "," + terceros + ",'" + nombre + "');"
                        c.execute(cosulta)
                        db.commit()
                        c.close()
                        mensaje = 'Cuenta registrada con exito'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'registrarCuenta.html', dicci)
                    else:
                        mensaje = 'No puede registrar, cuenta ya registrada'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'registrarCuenta.html', dicci)
                else:
                    mensaje = 'No puede registrar cuentas del mismo usuario'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'registrarCuenta.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'registrarCuenta.html', dicci)


def transferencias(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    if request.method == 'GET':
        mensaje = 'Seleccionar Opcion'
        dicci = {'titulo': mensaje}
        return render(request, 'transferencias.html', dicci)
    else:
        datos = request.POST
        filtro = datos.get('Cambio')
        transferir = datos.get('Transferir')
        if filtro is not None:
            if filtro == 'Propio':
                cosulta = "select codigo, tipo, moneda, monto from cuenta where usuario = " + usuario + " and tipo != 'plazo fijo' ;"
                c.execute(cosulta)
                cuentas1 = c.fetchall()
                cosulta = "select codigo,tipo, moneda, monto from cuenta where usuario = " + usuario + ";"
                c.execute(cosulta)
                cuentas2 = c.fetchall()
                mensaje = 'Cuentas Propias'
                variable = True
                dicci = {'titulo': mensaje, 'cuentas1': cuentas1, 'cuentas2': cuentas2, 'variable1': variable}
                return render(request, 'transferencias.html', dicci)
            elif filtro == 'Tercero':
                cosulta = "select codigo, tipo, moneda, monto from cuenta where usuario = " + usuario + " and tipo != 'plazo fijo' ;"
                c.execute(cosulta)
                cuentas1 = c.fetchall()
                cosulta = "select cuenta, nombre from cuenta_tercero where usuario = " + usuario + ";"
                c.execute(cosulta)
                cuentas3 = c.fetchall()
                mensaje = 'Cuentas a terceros'
                variable = True
                dicci = {'titulo': mensaje, 'cuentas1': cuentas1, 'cuentas3': cuentas3, 'variable2': variable}
                return render(request, 'transferencias.html', dicci)
        elif transferir is not None:
            mensaje = 'Transferencia Hecha'
            dicci = {'mensaje': mensaje}
            return render(request, 'transferencias.html', dicci)


def preCheque(request):
    usuario = str(request.session['usuario'])
    if request.method == 'GET':
        form = chequeForm()
        dicci = {'form': form}
        return render(request, 'preCheques.html', dicci)
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
                      "and cuenta.codigo = " + cuenta + " and chequera.codigo = " + chequera + " and " \
                                                                                               "cheque.codigo = " + cheque + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Datos incorrectos, cuenta, chequera o cheque inexistente'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'preCheques.html', dicci)
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
                        return render(request, 'preCheques.html', dicci)
                    else:
                        if float(monto) > float(monto_cuenta):
                            mensaje = 'Monto no disponible en la cuenta'
                            dicci = {'form': form, 'mensaje': mensaje}
                            return render(request, 'preCheques.html', dicci)
                        else:
                            if preautorizacion == 0:
                                mensaje = 'No tiene la preautorizacion de Cheques activa'
                                dicci = {'form': form, 'mensaje': mensaje}
                                return render(request, 'preCheques.html', dicci)
                            else:
                                cosulta = "select * from precheque where codigo = " + cheque + " and chequera = " + \
                                          chequera + " and estado ='emitido' ;"
                                c.execute(cosulta)
                                retorno = c.fetchone()
                                if retorno is None:
                                    cosulta = "insert into precheque values(" + str(cheque) + "," + str(chequera) + "" \
                                              ", 'emitido'," + str(monto) + ",'" + str(receptor) + "');"
                                    c.execute(cosulta)
                                    db.commit()
                                    c.close()
                                    mensaje = 'Cheque preautorizado con exito'
                                    dicci = {'form': form, 'mensaje': mensaje}
                                    return render(request, 'preCheques.html', dicci)
                                else:
                                    mensaje = 'El cheque ya ha sido preautorizado'
                                    dicci = {'form': form, 'mensaje': mensaje}
                                    return render(request, 'preCheques.html', dicci)
                else:
                    mensaje = 'La cuenta esta bloqueada, no se puede hacer transaccion de ningun tipo'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'preCheques.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'preCheques.html', dicci)


def estadoTar(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from c_individual inner join usuario on c_individual.usuario = usuario.codigo where usuario ="+ usuario + ";"
    c.execute(cosulta)
    retorno = c.fetchone()
    nombre = retorno[2]
    cui = str(retorno[0])
    nit = str(retorno[1])
    direccion = retorno[3]
    if request.method == 'GET':
        cosulta = "select * from tcredito where usuario = " + usuario + ";"
        c.execute(cosulta)
        retorno = c.fetchall()
        lista = ConvertirTarjeta(retorno)
        dicci = {'cuentas': lista, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
        return render(request, 'estadoTarjeta.html', dicci)
    else:
        datos = request.POST
        histo = datos.get('Historial')
        request.session['tarjeta'] = histo
        return redirect('historialT')


def ConvertirTarjeta(retorno):
    lista = []
    for tupla in retorno:
        lista.append(list(tupla))
    for elementos in lista:
        if elementos[4] == 'prefepuntos':
            elementos.append(True)
        else:
            elementos.append(False)
    return lista


def historialT(request):
    usuario = str(request.session['usuario'])
    tarjeta = str(request.session['tarjeta'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from transtarjeta where tarjeta = " + tarjeta + ";"
    c.execute(cosulta)
    retorno = c.fetchall()
    mensaje = tarjeta
    dicci = {'cuentas': retorno, 'titulo': mensaje}
    return render(request, 'historialTarjeta.html', dicci)


def prestamo(request):
    usuario = str(request.session['usuario'])
    if request.method == 'GET':
        form = PrestamoForm()
        dicci = {'form': form}
        return render(request, 'prestamos.html', dicci)
    else:
        form = PrestamoForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            monto = datos.get('monto')
            descripcion = datos.get('descripcion')
            plazo = datos.get('plazo')
            calcular = datos.get('Calcular')
            solicitar = datos.get('Solicitar')
            if calcular is not None:
                lista = CalcularPrestamo(float(monto))
                mensaje = 'Puede modificar la informacion antes de enviarla'
                dicci = {'form': form, 'mensaje': mensaje, 'prestamos': lista, 'variable1': True}
                return render(request, 'prestamos.html', dicci)
            if solicitar is not None:
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                c = db.cursor()
                cosulta = "insert into soliprestamo (monto, descripcion, plazo, estado, usuario) values (" + str(monto) + ",'" + str(descripcion) \
                + "'," + str(plazo) + ",'enviado'," + str(usuario) + ");"
                c.execute(cosulta)
                db.commit()
                mensaje = 'Prestamo solicitado con exito'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'prestamos.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'prestamos.html', dicci)


def estadoPres(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from c_individual inner join usuario on c_individual.usuario = usuario.codigo where usuario ="+ usuario + ";"
    c.execute(cosulta)
    retorno = c.fetchone()
    nombre = retorno[2]
    cui = str(retorno[0])
    nit = str(retorno[1])
    direccion = retorno[3]
    if request.method == 'GET':
        cosulta = "select * from tcredito where usuario = " + usuario + ";"
        c.execute(cosulta)
        retorno = c.fetchall()
        lista = ConvertirTarjeta(retorno)
        dicci = {'cuentas': lista, 'nombre': nombre, 'cui': cui, 'nit': nit, 'direccion': direccion}
        return render(request, 'estadoTarjeta.html', dicci)
    else:
        datos = request.POST
        histo = datos.get('Historial')
        request.session['tarjeta'] = histo
        return redirect('historialT')


def cuotasPres(request):
    usuario = str(request.session['usuario'])
    tarjeta = str(request.session['tarjeta'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from transtarjeta where tarjeta = " + tarjeta + ";"
    c.execute(cosulta)
    retorno = c.fetchall()
    mensaje = tarjeta
    dicci = {'cuentas': retorno, 'titulo': mensaje}
    return render(request, 'historialTarjeta.html', dicci)


def estadoCEm(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from c_empresarial inner join usuario on c_empresarial.usuario = usuario.codigo where usuario =" + usuario + ";"
    c.execute(cosulta)
    retorno = c.fetchone()
    nombre = retorno[1]
    representante = retorno[3]
    nit = str(retorno[0])
    direccion = retorno[4]
    if request.method == 'GET':
        cosulta = "select cuenta.codigo, cuenta.tipo, c_empresarial.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                  "from c_empresarial, usuario, cuenta where c_empresarial.usuario = usuario.codigo and " \
                  "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + ";"
        c.execute(cosulta)
        retorno = c.fetchall()
        lista = ConvertirTupla(retorno)
        mensaje = 'Cuentas'
        dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'representante': representante, 'nit': nit, 'direccion': direccion}
        return render(request, 'empresarial/estadoCuenta.html', dicci)
    else:
        datos = request.POST
        filtro = datos.get('Ingresar')
        bloqueo = datos.get('Bloqueo')
        histo = datos.get('Historial')
        if filtro is not None:
            if filtro == 'Monetaria':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_empresarial.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_empresarial, usuario, cuenta where c_empresarial.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'monetaria' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas Monetarias'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'representante': representante, 'nit': nit, 'direccion': direccion}
                return render(request, 'empresarial/estadoCuenta.html', dicci)
            elif filtro == 'Ahorro':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_empresarial.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_empresarial, usuario, cuenta where c_empresarial.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'ahorro' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas de ahorro'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'representante': representante, 'nit': nit, 'direccion': direccion}
                return render(request, 'empresarial/estadoCuenta.html', dicci)
            elif filtro == 'Plazo':
                cosulta = "select cuenta.codigo, cuenta.tipo, c_empresarial.nombre, cuenta.moneda, cuenta.monto, cuenta.estado " \
                          "from c_empresarial, usuario, cuenta where c_empresarial.usuario = usuario.codigo and " \
                          "usuario.codigo = cuenta.usuario and usuario.codigo = " + usuario + " " \
                          " and cuenta.tipo = 'plazo fijo' ;"
                c.execute(cosulta)
                retorno = c.fetchall()
                lista = ConvertirTupla(retorno)
                mensaje = 'Cuentas Plazo Fijo'
                dicci = {'cuentas': lista, 'titulo': mensaje, 'nombre': nombre, 'representante': representante, 'nit': nit, 'direccion': direccion}
                return render(request, 'empresarial/estadoCuenta.html', dicci)
        elif bloqueo is not None:
            cosulta = "select estado from cuenta where codigo = " + bloqueo + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            print(retorno)
            if retorno[0] == 1:
                consulta = 'update cuenta set estado = 0 where codigo = ' + bloqueo + ';'
                print(consulta)
                c.execute(consulta)
                db.commit()
                c.close()
            else:
                consulta = 'update cuenta set estado = 1 where codigo = ' + bloqueo + ';'
                c.execute(consulta)
                db.commit()
                c.close()
            return redirect('estadoCuentaEm')
        elif histo is not None:
            cosulta = "select moneda from cuenta where codigo = " + histo + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            request.session['cuenta'] = histo
            request.session['moneda'] = retorno[0]
            return redirect('historialEm')


def historialEm(request):
    usuario = str(request.session['usuario'])
    cuenta = str(request.session['cuenta'])
    moneda = request.session['moneda']
    print(cuenta)
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    cosulta = "select * from transaccion where cuenta =" + cuenta + ";"
    c.execute(cosulta)
    retorno = c.fetchall()
    mensaje = cuenta
    dicci = {'cuentas': retorno, 'titulo': mensaje, 'moneda': moneda}
    return render(request, 'empresarial/historial.html', dicci)


def nuevaCEm(request):
    usuario = str(request.session['usuario'])
    if request.method == 'GET':
        form = AgregarUsuarioForm()
        dicci = {'form': form}
        return render(request, 'empresarial/registrarCuenta.html', dicci)
    else:
        form = AgregarUsuarioForm(data=request.POST)
        if form.is_valid():
            datos = request.POST
            cuenta = datos.get('cuenta')
            nombre = datos.get('nombre')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            cosulta = 'select codigo, usuario from cuenta where codigo =' + cuenta + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Cuenta no existe'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'empresarial/registrarCuenta.html', dicci)
            else:
                terceros = str(retorno[0])
                usuario_cuenta = str(retorno[1])
                if usuario != usuario_cuenta:
                    cosulta = "select * from cuenta_tercero where usuario = " + usuario + " and cuenta = " + terceros + ";"
                    c.execute(cosulta)
                    retorno = c.fetchone()
                    if retorno is None:
                        cosulta = "insert into cuenta_tercero values(" + usuario + "," + terceros + ",'" + nombre + "');"
                        c.execute(cosulta)
                        db.commit()
                        c.close()
                        mensaje = 'Cuenta registrada con exito'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'empresarial/registrarCuenta.html', dicci)
                    else:
                        mensaje = 'No puede registrar, cuenta ya registrada'
                        dicci = {'form': form, 'mensaje': mensaje}
                        return render(request, 'empresarial/registrarCuenta.html', dicci)
                else:
                    mensaje = 'No puede registrar cuentas del mismo usuario'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'empresarial/registrarCuenta.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'empresarial/registrarCuenta.html', dicci)


def transferenciasEm(request):
    usuario = str(request.session['usuario'])
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    if request.method == 'GET':
        mensaje = 'Seleccionar Opcion'
        dicci = {'titulo': mensaje}
        return render(request, 'empresarial/transferencias.html', dicci)
    else:
        datos = request.POST
        filtro = datos.get('Cambio')
        transferir = datos.get('Transferir')
        if filtro is not None:
            if filtro == 'Propio':
                cosulta = "select codigo, tipo, moneda, monto from cuenta where usuario = " + usuario + " and tipo != 'plazo fijo' ;"
                c.execute(cosulta)
                cuentas1 = c.fetchall()
                cosulta = "select codigo,tipo, moneda, monto from cuenta where usuario = " + usuario + ";"
                c.execute(cosulta)
                cuentas2 = c.fetchall()
                mensaje = 'Cuentas Propias'
                variable = True
                dicci = {'titulo': mensaje, 'cuentas1': cuentas1, 'cuentas2': cuentas2, 'variable1': variable}
                return render(request, 'empresarial/transferencias.html', dicci)
            elif filtro == 'Tercero':
                cosulta = "select codigo, tipo, moneda, monto from cuenta where usuario = " + usuario + " and tipo != 'plazo fijo' ;"
                c.execute(cosulta)
                cuentas1 = c.fetchall()
                cosulta = "select cuenta, nombre from cuenta_tercero where usuario = " + usuario + ";"
                c.execute(cosulta)
                cuentas3 = c.fetchall()
                mensaje = 'Cuentas a terceros'
                variable = True
                dicci = {'titulo': mensaje, 'cuentas1': cuentas1, 'cuentas3': cuentas3, 'variable2': variable}
                return render(request, 'empresarial/transferencias.html', dicci)
        elif transferir is not None:
            mensaje = 'Transferencia Hecha'
            dicci = {'mensaje': mensaje}
            return render(request, 'empresarial/transferencias.html', dicci)


def preChequeEm(request):
    usuario = str(request.session['usuario'])
    if request.method == 'GET':
        form = chequeForm()
        dicci = {'form': form}
        return render(request, 'empresarial/preCheques.html', dicci)
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
                      "and cuenta.codigo = " + cuenta + " and chequera.codigo = " + chequera + " and " \
                                                                                               "cheque.codigo = " + cheque + ";"
            c.execute(cosulta)
            retorno = c.fetchone()
            if retorno is None:
                mensaje = 'Datos incorrectos, cuenta, chequera o cheque inexistente'
                dicci = {'form': form, 'mensaje': mensaje}
                return render(request, 'empresarial/preCheques.html', dicci)
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
                        return render(request, 'empresarial/preCheques.html', dicci)
                    else:
                        if float(monto) > float(monto_cuenta):
                            mensaje = 'Monto no disponible en la cuenta'
                            dicci = {'form': form, 'mensaje': mensaje}
                            return render(request, 'empresarial/preCheques.html', dicci)
                        else:
                            if preautorizacion == 0:
                                mensaje = 'No tiene la preautorizacion de Cheques activa'
                                dicci = {'form': form, 'mensaje': mensaje}
                                return render(request, 'empresarial/preCheques.html', dicci)
                            else:
                                cosulta = "select * from precheque where codigo = " + cheque + " and chequera = " + \
                                          chequera + " and estado ='emitido' ;"
                                c.execute(cosulta)
                                retorno = c.fetchone()
                                if retorno is None:
                                    cosulta = "insert into precheque values(" + str(cheque) + "," + str(chequera) + "" \
                                              ", 'emitido'," + str(monto) + ",'" + str(receptor) + "');"
                                    c.execute(cosulta)
                                    db.commit()
                                    c.close()
                                    mensaje = 'Cheque preautorizado con exito'
                                    dicci = {'form': form, 'mensaje': mensaje}
                                    return render(request, 'empresarial/preCheques.html', dicci)
                                else:
                                    mensaje = 'El cheque ya ha sido preautorizado'
                                    dicci = {'form': form, 'mensaje': mensaje}
                                    return render(request, 'empresarial/preCheques.html', dicci)
                else:
                    mensaje = 'La cuenta esta bloqueada, no se puede hacer transaccion de ningun tipo'
                    dicci = {'form': form, 'mensaje': mensaje}
                    return render(request, 'empresarial/preCheques.html', dicci)
        else:
            mensaje = 'Datos incompletos y/o incorrectos'
            dicci = {'form': form, 'mensaje': mensaje}
            return render(request, 'empresarial/preCheques.html', dicci)


def CalcularPrestamo(monto):
    if monto <= 5000.00:
        lista = []
        lista1 = []
        cuota1 = monto / 12
        interes = cuota1 * 0.05
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('5%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 24
        interes = cuota1 * 0.04
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('4%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 36
        interes = cuota1 * 0.0335
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('3.35%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 48
        interes = cuota1 * 0.025
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('2.5%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        return lista
    elif 5000.00 < monto <= 15000.00:
        lista = []
        lista1 = []
        cuota1 = monto / 12
        interes = cuota1 * 0.0525
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('5.25%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 24
        interes = cuota1 * 0.0415
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('4.15%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 36
        interes = cuota1 * 0.0350
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('3.5%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 48
        interes = cuota1 * 0.026
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('2.6%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        return lista
    elif 15000.00 < monto <= 30000.00:
        lista = []
        lista1 = []
        cuota1 = monto / 12
        interes = cuota1 * 0.053
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('5.30%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 24
        interes = cuota1 * 0.042
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('4.20%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 36
        interes = cuota1 * 0.0355
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('3.55%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 48
        interes = cuota1 * 0.065
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('2.65%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        return lista
    elif 30000.00 < monto <= 60000.00:
        lista = []
        lista1 = []
        cuota1 = monto / 12
        interes = cuota1 * 0.0535
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('5.35%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 24
        interes = cuota1 * 0.0425
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('4.25%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 36
        interes = cuota1 * 0.0360
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('3.60%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 48
        interes = cuota1 * 0.0270
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('2.70%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        return lista
    elif monto > 60000.00:
        lista = []
        lista1 = []
        cuota1 = monto / 12
        interes = cuota1 * 0.0545
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('5.45%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 24
        interes = cuota1 * 0.0435
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('4.35%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 36
        interes = cuota1 * 0.0370
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('3.70%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        lista1 = []
        cuota1 = monto / 48
        interes = cuota1 * 0.0280
        total = cuota1 + interes
        lista1.append(round(monto, 2))
        lista1.append(12)
        lista1.append(round(cuota1, 2))
        lista1.append('2.80%')
        lista1.append(round(total, 2))
        lista.append(lista1)
        return lista


def planillas(request):
    return render(request, 'planillas.html')


def proveedores(request):
    return render(request, 'proveedores.html')

