# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CEmpresarial(models.Model):
    nit = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    nombre_comercial = models.CharField(max_length=45)
    representante = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    tipo = models.ForeignKey('TipoEmpresa', models.DO_NOTHING, db_column='tipo')

    class Meta:
        managed = False
        db_table = 'c_empresarial'


class CIndividual(models.Model):
    cui = models.BigIntegerField(primary_key=True)
    nit = models.IntegerField()
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'c_individual'


class Cheque(models.Model):
    codigo = models.IntegerField(primary_key=True)
    chequera = models.ForeignKey('Chequera', models.DO_NOTHING, db_column='chequera')
    estado = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'cheque'
        unique_together = (('codigo', 'chequera'),)


class Chequera(models.Model):
    codigo = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    cuenta = models.ForeignKey('Cuenta', models.DO_NOTHING, db_column='cuenta', related_name='+')

    class Meta:
        managed = False
        db_table = 'chequera'


class Cuenta(models.Model):
    codigo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    estado = models.IntegerField()
    moneda = models.CharField(max_length=1)
    pre_cheques = models.IntegerField()
    interes = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    plazo = models.CharField(max_length=45, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'cuenta'


class CuentaTercero(models.Model):
    usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='usuario', primary_key=True)
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='cuenta')

    class Meta:
        managed = False
        db_table = 'cuenta_tercero'
        unique_together = (('usuario', 'cuenta'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Precheque(models.Model):
    codigo = models.OneToOneField(Cheque, models.DO_NOTHING, db_column='codigo', primary_key=True)
    chequera = models.ForeignKey(Cheque, models.DO_NOTHING, db_column='chequera', related_name='+')
    estado = models.CharField(max_length=45)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    destinatario = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'precheque'
        unique_together = (('codigo', 'chequera'),)


class Promocion(models.Model):
    codigo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='cuenta')

    class Meta:
        managed = False
        db_table = 'promocion'


class TarjetaDebito(models.Model):
    numero = models.AutoField(primary_key=True)
    seguridad = models.IntegerField()
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='cuenta')

    class Meta:
        managed = False
        db_table = 'tarjeta_debito'


class TipoEmpresa(models.Model):
    abreviacion = models.CharField(primary_key=True, max_length=45)
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_empresa'


class Transaccion(models.Model):
    codigo_autorizacion = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=150)
    tipo = models.CharField(max_length=30)
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='cuenta')

    class Meta:
        managed = False
        db_table = 'transaccion'
        unique_together = (('codigo_autorizacion', 'cuenta'),)


class Usuario(models.Model):
    codigo = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=45)
    tipo = models.IntegerField()
    estado = models.IntegerField()
    intentos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuario'
