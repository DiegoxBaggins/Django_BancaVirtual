"""ProyectoBanca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index1'),
    path('inicio', views.inicio, name='inicioNormal'),
    path('empresarial/inicio', views.inicioEm, name='inicioEmpresarial'),
    path('transferencias', views.transferencias, name='transferencias'),
    path('estadoCuenta', views.estadoC, name='estadoCuenta'),
    path('estadoCuenta/historial', views.historial, name='historial'),
    path('nuevaCuenta', views.nuevaC, name='cuentaTerceros'),
    path('preCheque', views.preCheque, name='preautorizar'),
    path('tarjetas', views.estadoTar, name='tarjetas'),
    path('tarjetas/historial',views.historialT, name='historialT'),
    path('prestamo', views.solicitarPrestamo, name='prestamo'),
    path('misPrestamos', views.estadoPres, name='estadoPrestamo'),
    path('misPrestamos/cuotas', views.cuotasPres, name='cuotasEs'),

    path('empresarial/transferencias', views.transferenciasEm, name='transferenciasEm'),
    path('empresarial/estadoCuenta', views.estadoCEm, name='estadoCuentaEm'),
    path('empresarial/estadoCuenta/historial', views.historialEm, name='historialEm'),
    path('empresarial/nuevaCuenta', views.nuevaCEm, name='cuentaTercerosEm'),
    path('empresarial/preCheque', views.preChequeEm, name='preautorizarEm'),

    path('planillas', views.planillas, name='planillas'),
    path('proveedores', views.proveedores, name='proveedores'),

]
