create database djangodic;
use djangodic;

create table djangodic.usuario (
codigo int not null,
password varchar(45) not null,
tipo int not null,
estado tinyint not null,
intentos tinyint not null,
tarjetas tinyint not null,
primary key (codigo)
);

create table djangodic.tipo_empresa (
abreviacion varchar(45) not null,
nombre varchar(45) not null,
primary key (abreviacion)
);

create table djangodic.c_individual (
cui bigint not null,
nit int not null,
nombre varchar(45) not null,
direccion varchar(45) not null,
usuario int not null,
primary key (cui),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.c_empresarial (
nit int not null,
nombre varchar(45) not null,
nombre_comercial varchar(45) not null,
representante varchar(45) not null,
direccion varchar(45) not null,
usuario int not null,
tipo varchar(45) not null,
primary key (nit),
foreign key (usuario) references usuario(codigo),
foreign key (tipo) references tipo_empresa(abreviacion)
);

create table djangodic.cuenta (
codigo int auto_increment not null,
tipo varchar(10) not null,
monto decimal(15,2) not null,
estado TinyInt not null,
moneda varchar(1) not null,
pre_cheques TinyInt not null,
interes decimal(5,3),
plazo varchar(45),
fecha_inicio date,
usuario int not null,
primary key (codigo),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.cuenta_tercero (
usuario int not null,
cuenta int not null,
nombre varchar(50) not null,
primary key (usuario, cuenta),
foreign key (usuario) references usuario(codigo),
foreign key (cuenta) references cuenta(codigo)
);

create table djangodic.chequera (
codigo int auto_increment not null,
cantidad int not null,
cuenta int not null,
primary key (codigo),
foreign key (cuenta) references cuenta(codigo)
);

create table djangodic.cheque (
codigo int not null,
chequera int not null,
estado varchar(45) not null,
primary key (codigo, chequera),
foreign key (chequera) references chequera(codigo)
);

create table djangodic.precheque(
codigo int not null,
chequera int not null,
estado varchar(45) not null,
monto decimal(10,2) not null,
destinatario varchar(75) not null,
primary key (codigo, chequera),
foreign key (codigo) references cheque(codigo),
foreign key (chequera) references cheque(chequera)
);

create table djangodic.transaccion (
codigo_autorizacion int auto_increment not null,
monto decimal(15,2) not null,
fecha date not null,
descripcion varchar(150) not null,
tipo varchar(30) not null,
cuenta int not null,
primary key (codigo_autorizacion, cuenta),
foreign key (cuenta) references cuenta(codigo)
);

create table djangodic.tcredito (
numero int auto_increment not null,
seguridad int not null,
limite decimal(14,2) not null,
gasto decimal(14,2) not null,
marca varchar(40) not null,
usuario int not null,
primary key (numero),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.transtarjeta (
codigo_autorizacion int auto_increment not null,
monto decimal (14,2) not null,
fecha date not null,
descripcion varchar(250) not null,
tipo varchar(50) not null,
porcentaje decimal (4,3) not null,
tarjeta int not null,
primary key (codigo_autorizacion),
foreign key (tarjeta) references tcredito(numero)
);

create table djangodic.compra (
codigo int not null,
descripcion varchar(250) not null,
fecha date not null,
moneda varchar(10) not null,
monto decimal(14,2) not null,
usuario int not null,
transaccion int not null,
primary key (codigo),
foreign key (transaccion) references transtarjeta(codigo_autorizacion),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.soliprestamo (
codigo int auto_increment not null,
monto decimal (12,2) not null,
descripcion varchar(250) not null,
plazo int not null,
estado varchar(50) not null,
usuario int not null,
primary key (codigo),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.prestamo (
codigo int auto_increment not null,
monto decimal (12,2) not null,
descripcion varchar(250) not null,
plazo int not null,
estado varchar(50) not null,
cuota decimal (12,2) not null,
interes decimal (5,2) not null,
usuario int not null,
solicitud int not null,
primary key (codigo),
foreign key (usuario) references usuario(codigo),
foreign key (solicitud) references soliprestamo(codigo)
);

create table djangodic.cuotas (
prestamo int not null,
cuota int not null,
estado varchar(50) not null,
monto decimal (12,2) not null,
interes decimal (5,2) not null,
primary key (prestamo, cuota),
foreign key (prestamo) references prestamo(codigo)
);