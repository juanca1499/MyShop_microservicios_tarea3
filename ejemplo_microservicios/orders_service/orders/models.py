from django.db import models

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: models.py
#
# Descripción:
#
#   En este archivo se definen los modelos para la app del Catálogo
#
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |                        |
#           |                       |  - Representa la        |  - Se indica los       |
#           |                       |    orden que se crea    |    campos del modelo   |
#           |         Order         |    con los datos del    |    así como sus pro-   |
#           |                       |    cliente para fina-   |    piedades.           |
#           |                       |    lizar la compra.     |                        |
#           |                       |                         |                        |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |                        |
#           |                       |  - Representa cada uno  |  - Se indica los       |
#           |                       |    de los items de la   |    campos del modelo   |
#           |       OrderItem       |    orden, los cuales    |    así como sus pro-   |
#           |                       |    vienen de los items  |    piedades.           |
#           |                       |    del carrito.         |                        |
#           |                       |                         |                        |
#           +-----------------------+-------------------------+------------------------+
#
#-------------------------------------------------------------------------

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=15, decimal_places=2)

    # Clase Meta en donde se indican campos para ordenamiento.
    class Meta:
        ordering = ('-created',)

    # Método to String de la clase, la cual es representada por el campo 'id'.
    def __str__(self):
        return 'Order {}'.format(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=11, decimal_places=2)