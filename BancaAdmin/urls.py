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
    path('', views.index, name='index'),
    path('inicio', views.inicio, name='inicio'),
    path('nuevoCliente', views.nuevoCliente, name='nuevoCliente'),
    path('nuevoCliente/individual', views.nuevoIndividual, name='nuevoIndividual'),
    path('nuevoCliente/Empresarial', views.nuevoEmpresarial, name='nuevoEmpresarial'),
    path('nuevaCuenta', views.nuevaCuenta, name='nuevaCuenta'),
    path('nuevaCuenta/Monetaria', views.nuevaMonetaria, name='nuevaMonetaria'),
    path('nuevaCuenta/Ahorro', views.nuevaAhorro, name='nuevaAhorro'),
    path('nuevaCuenta/PlazoFijo', views.nuevaPlazo, name='nuevaPlazo'),
    path('nuevaChequera', views.nuevaChequera, name='nuevaChequera'),
    path('desbloquear', views.desbloqueo, name='desbloqueo'),
    path('deposito', views.deposito, name='deposito'),
    path('cambioCheque', views.cambioCheque, name='cambioCheque'),
]
