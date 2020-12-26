create database djangodic;
use djangodic;

create table djangodic.usuario (
codigo int not null,
password varchar(45) not null,
tipo int not null,
estado tinyint not null,
intentos tinyint not null,
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

create table djangodic.promocion(
codigo int not null,
descripcion varchar(150) not null,
fecha_inicio date not null,
fecha_final date not null,
cuenta int not null,
primary key(codigo),
foreign key (cuenta) references cuenta(codigo)
);

create table djangodic.tarjeta_debito(
numero int auto_increment not null,
seguridad int not null,
cuenta int not null,
primary key (numero),
foreign key (cuenta) references cuenta(codigo)
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
