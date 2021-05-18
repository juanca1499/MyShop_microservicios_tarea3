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
from .views import CartViewSet

urlpatterns = [
    path('info/<str:session_id>', CartViewSet.as_view({
        'get': 'retrieve'
    })),
    path('items', CartViewSet.as_view({
        'post': 'add_item'
    })),
    path('items/<str:session_id>', CartViewSet.as_view({
        'get': 'items_list',
    })),
    path('items-qty/<str:session_id>', CartViewSet.as_view({
        'get': 'get_items_qty',
    })),
    path('total/<str:session_id>', CartViewSet.as_view({
        'get': 'get_cart_total'
    })),
    path('items/<str:session_id>/<int:product_id>', CartViewSet.as_view({
        'post': 'update_item',
        'delete': 'remove_item'
    }))
]