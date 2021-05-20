#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: urls.py
#
# Descripción:
#   En este archivo se definen las urls de la app de las órdenes.
#
#   Cada url debe tener la siguiente estructura:
#
#   path( url, vista, nombre_url )
#
#-------------------------------------------------------------------------

from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path('order', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('order/delete/<str:pk>', OrderViewSet.as_view({
        'get': 'confirm',
        'delete': 'destroy'
    })),
    path('order/<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy'
    })),
    path('order/items/<str:pk>', OrderViewSet.as_view({
        'get': 'items_list',
        'post': 'update_order'
    })),
    path('order/flag/<str:pk>', OrderViewSet.as_view({
        'get': 'time_verify',
    })),  
]