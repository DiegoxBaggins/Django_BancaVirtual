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
bono decimal(14,2) not null,
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
interes decimal (10,2) not null,
fecha date not null,
pago decimal (12,2) not null,
primary key (prestamo, cuota),
foreign key (prestamo) references prestamo(codigo)
);

create table djangodic.planilla (
cuenta int not null,
nombre varchar(200) not null,
sueldo decimal(10,2) not null,
forma varchar(50),
usuario int not null,
primary key (cuenta, usuario),
foreign key (cuenta) references cuenta(codigo),
foreign key (usuario) references usuario(codigo)
);

create table djangodic.proveedor (
cuenta int not null,
nombre varchar(200) not null,
sueldo decimal(10,2) not null,
forma varchar(50),
usuario int not null,
primary key (cuenta, usuario),
foreign key (cuenta) references cuenta(codigo),
foreign key (usuario) references usuario(codigo)
);


insert into usuario values(1022,'1022',0,1,0,0);

insert into tipo_empresa values ('Com', 'Comida');
insert into tipo_empresa values ('Sum', 'Suministros');

#empresariales
insert into usuario values (404040, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404040, 'Bimbo', 'Bimbo INC', 'Juan', 'Guatemala', 404040, 'Com');
insert into cuenta values(404040, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 404040);

insert into usuario values (404041, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404041, 'Tortrix', 'Tortrix INC', 'Juan', 'Guatemala', 404041, 'Com');
insert into cuenta values(404041, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 404041);

insert into usuario values (404042, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404042, 'Dollar City', 'Dollar INC', 'Juan', 'Guatemala', 404042, 'Sum');
insert into cuenta values(404042, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 404042);

insert into usuario values (404043, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404043, 'Office Depot', 'Depot INC', 'Juan', 'Guatemala', 404043, 'Sum');
insert into cuenta values(404043, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 404043);

insert into usuario values (404044, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404044, 'Cemaco', 'Cemaco INC', 'Juan', 'Guatemala', 404044, 'Sum');
insert into cuenta values(404044, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 404044);

#empresa1
insert into usuario values (404045, '1010', 2, 1, 0, 0);
insert into c_empresarial values(404045, 'Genetik', 'Genetik INC', 'Diego', 'Guatemala', 404045, 'Sum');
insert into cuenta values(404045, 'monetaria', 1000000.00, 1, 'Q', 0, null, null, null, 404045);

#personales
insert into usuario values (303040, '3030', 1, 1, 0, 0);
insert into c_individual values(303040, 303040, 'Diego', 'Guatemala', 303040);
insert into cuenta values(303040, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 303040);

insert into usuario values (303041, '3030', 1, 1, 0, 0);
insert into c_individual values(303041, 303041, 'Mario', 'Guatemala', 303041);
insert into cuenta values(303041, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 303041);

insert into usuario values (303042, '3030', 1, 1, 0, 0);
insert into c_individual values(303042, 303042, 'Luis', 'Guatemala', 303042);
insert into cuenta values(303042, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 303042);

#personalesCSV
insert into usuario values (541234, '3030', 1, 1, 0, 0);
insert into c_individual values(541234, 303040, 'DIEGO FERNANDO CORTES LOPEZ', 'Guatemala', 541234);
insert into cuenta values(541234, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 541234);

insert into usuario values (263769, '3030', 1, 1, 0, 0);
insert into c_individual values(263769, 263769, 'KARINA NOHEMI RAMIREZ ORELLANA', 'Guatemala', 263769);
insert into cuenta values(263769, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 263769);

insert into usuario values (481366, '3030', 1, 1, 0, 0);
insert into c_individual values(481366, 481366, 'ANGEL GEOVANY ARAGON PEREZ', 'Guatemala', 481366);
insert into cuenta values(481366, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 481366);

insert into usuario values (152352, '3030', 1, 1, 0, 0);
insert into c_individual values(152352, 152352, 'CARLOS ROBERTO QUIXTAN PEREZ', 'Guatemala', 152352);
insert into cuenta values(152352, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 152352);

insert into usuario values (358054, '3030', 1, 1, 0, 0);
insert into c_individual values(358054, 358054, 'ERICK IVAN MAYORGA RODRIGUEZ', 'Guatemala', 358054);
insert into cuenta values(358054, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 358054);

insert into usuario values (503944, '3030', 1, 1, 0, 0);
insert into c_individual values(503944, 503944, 'BYRON ESTUARDO CAAL CATUN', 'Guatemala', 503944);
insert into cuenta values(503944, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 503944);

insert into usuario values (316167, '3030', 1, 1, 0, 0);
insert into c_individual values(316167, 316167, 'RONALD RODRIGO MARIN SALAS', 'Guatemala', 316167);
insert into cuenta values(316167, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 316167);

insert into usuario values (374296, '3030', 1, 1, 0, 0);
insert into c_individual values(374296, 374296, 'OSCAR DANIEL OLIVA', 'Guatemala', 374296);
insert into cuenta values(374296, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 374296);

insert into usuario values (556658, '3030', 1, 1, 0, 0);
insert into c_individual values(556658, 556658, 'EDUARDO ABRAHAM BARILLAS', 'Guatemala', 556658);
insert into cuenta values(556658, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 556658);

insert into usuario values (462978, '3030', 1, 1, 0, 0);
insert into c_individual values(462978, 462978, 'CARLOS ESTUARDO MONTERROSO SANTOS', 'Guatemala', 462978);
insert into cuenta values(462978, 'monetaria', 100000.00, 1, 'Q', 0, null, null, null, 462978);