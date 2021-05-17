#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: urls.py
#
# Descripción:
#   En este archivo se definen las urls de la app del carrito de compras.
#
#   Cada url debe tener la siguiente estructura:
#
#   path( url, vista, nombre_url )
#
#-------------------------------------------------------------------------

from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail({
        'get': 'list',
        'post': 'create'
    })),
    path('add/<str:pk>', views.cart_add({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    })),
    path('remove/<str:pk>', views.cart_remove({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    }))
]