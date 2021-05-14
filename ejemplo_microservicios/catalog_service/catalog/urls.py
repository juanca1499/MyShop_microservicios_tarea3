#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: urls.py
#
# Implementación de Arquitecturas Microservicios.
# Autor(es): Perla Velasco & Jorge Alfonso Solís.
# Version: 1.0.0 Marzo 2021
#
# Descripción:
#   En este archivo se definen las urls de la app hello_django.
#
#-------------------------------------------------------------------------

from django.urls import path

from .views import ProductViewSet, CategoryViewSet

urlpatterns = [
    path('product', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('product/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('category', CategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('category/<str:pk>', CategoryViewSet.as_view({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    }))
]
