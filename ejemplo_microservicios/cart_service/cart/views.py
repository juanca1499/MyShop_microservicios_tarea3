#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------------
# Archivo: views.py
#
    
# Descripción:
#   En este archivo se definen las vistas para la app del carrito de compras del sistema.
#
#   A continuación se describen los métodos que se implementaron en este archivo:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - request: datos de     |  - Añade el producto  |
#           |                        |    la solicitud.         |    indicado al carrito|
#           |       cart_add()       |                          |    de compras con     |
#           |                        |  - product_id: id del    |    ayuda de la clase  |
#           |                        |    producto a agregar.   |    Cart.              |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - request: datos de     |  - Remueve el pro-    |
#           |                        |    la solicitud.         |    ducto indicado     |
#           |      cart_remove()     |                          |    del carrito con    |
#           |                        |  - product_id: id del    |    ayuda de la clase  |
#           |                        |    producto a remover.   |    Cart.              |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Obtiene los datos  |
#           |                        |  - request: datos de     |    necesarios para    |
#           |      cart_detail()     |    la solicitud.         |    mostrar el detalle |
#           |                        |                          |    del carrito de     |
#           |                        |                          |    compras.           |
#           +------------------------+--------------------------+-----------------------+
#
#--------------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
import decimal

from .models import CartItem, Cart
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    
    # Método que se accede por la URL /info/<str:session_id>
    def retrieve(self, request, session_id):
        # Se obtiene el carrito de la sesión
        cart = get_object_or_404(Cart,session_id=session_id)
        # Se crea el serializer
        serializer = CartSerializer(cart)
        # Se envía la respuesta a la solicitud
        return Response(serializer.data)

    # Método que se accede por la URL /cart/<str:session_id>
    def items_list(self, request, session_id):
        # Se obtiene el carrito de la sesión
        cart = get_object_or_404(Cart,session_id=session_id)
        #Se obtienen la lista de items
        cart_items = CartItem.objects.all()
        # Se filtran los items que corresponden al carrito de la sesión
        cart_items = cart_items.filter(cart=cart)
        # Se crea el serializer y se envía como response
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def get_items_qty(self, request, session_id):
        cart = get_object_or_404(Cart, session_id=session_id)
        cart_items = CartItem.objects.all()
        cart_items = cart_items.filter(cart=cart)

    def get_cart_total(self, request, session_id):
        # Se obtiene el carrito de la sesión
        cart = get_object_or_404(Cart,session_id=session_id)
        total = cart.total
        total_json = json.dumps(Decimal(total))
        return Response(total_json)

    # Método que se accede por la URL /items
    def add_item(self, request):
        session_id = request.data['session_id']
        product_id = request.data['product_id']
        product_name = request.data['product_name']
        product_image = request.data['product_image']
        product_price = float(request.data['product_price'])
        quantity = float(request.data['quantity'])
        price = product_price * quantity
        # Detectamos si la sesión ya tiene un carrito
        try:
            cart = Cart.objects.get(session_id=session_id)
        except:
            cart = None
            
        # Si no tiene un carrito, se le crea uno.
        if cart is None:
            cart = Cart()
            cart.session_id = session_id
            cart.total = 0.0
            cart.save()

        # Detectamos si el item elegido es uno ya existente en el carrito 
        try:
            cart_item = CartItem.objects.get(cart=cart,product_id=product_id)
        except:
            cart_item = None

        # Si el item no existía en el carrito, se crea uno nuevo.
        if cart_item is None:
            cart_item = CartItem()
            cart_item.cart = cart
            cart_item.product_id = product_id
            cart_item.name = product_name
            cart_item.image = product_image
            cart_item.unit_price = product_price
            cart_item.quantity = quantity
            cart_item.price = price
            cart_item.save()
            cart.total = decimal.Decimal(cart.total) + decimal.Decimal(cart_item.price)
        # Si ya existe, sólo se aumenta la cantidad solicitada.
        else:
            cart_item.quantity = cart_item.quantity + quantity
            amount_added = decimal.Decimal(quantity * product_price) 
            cart_item.price = cart_item.price + amount_added
            cart_item.save()
            cart.total = cart.total + amount_added

        # Actualizamos el total del carrito
        cart.save()
        # Se serializan los items agregados al carrito
        cart_items = CartItem.objects.filter(cart=cart)
        #Se crea el serializer y se envía como response
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Método que se accede por la URL /cart/<str:session_id>/<str:product_id>
    def update_item(self, request, session_id, product_id): 
        # Se obtiene el carrito
        cart = get_object_or_404(Cart,session_id=session_id)
        # Obtiene el cart_item que pertenece al carrito y al producto 
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        # Extrae la cantidad de la petición
        quantity = float(request.data['quantity'])
        # Se realiza el nuevo cambio en la cantidad
        cart_item.quantity = quantity
        # Se realizan los calculos correspondientes al precio
        cart.total= cart.total-cart_item.price
        cart_item.price = decimal.Decimal(quantity)*cart_item.unit_price
        cart.total= cart.total+cart_item.price
        cart.save()
        cart_item.save()
        # Se crea el serializer con los datos recibidos
        cart_items = CartItem.objects.filter(cart=cart)
        #Se crea el serializer y se envía como response
        serializer = CartItemSerializer(cart_items, many=True)
        # Se envía la respuesta a la solicitud
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

     # Método que se accede por la URL /cart/<str:session_id>/<str:product_id>
    def remove_item(self, request, session_id, product_id):
        # Se obtiene el carrito al cual pertenece el item
        cart = get_object_or_404(Cart,session_id=session_id)
        # Se busca el item en base al carrito y al id del producto
        cart_item = get_object_or_404(CartItem,cart=cart,product_id=product_id)
        # Se resta la cantidad total a pagar
        cart.total = cart.total - cart_item.price
        cart.save()
        # Se procede a eliminar el item del carrito
        cart_item.delete()
        # Se envía la respuesta a la solicitud
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Método que se accede por la URL /product/<str:pk>
    def destroy(self, request, session_id):
        # Se obtiene el producto con ayuda del pk recibido
        cart = Cart.objects.get(session_id=session_id)
        # Se procede a eliminar el producto
        cart.delete()
        # Se envía la respuesta a la solicitud
        return Response(status=status.HTTP_204_NO_CONTENT)
