#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: models.py
#
# Autor(es): Perla Velasco & Jorge Alfonso Solís.
# Version: 1.0.0 Marzo 2021
#
# Descripción:
#
#   En este archivo se definen los modelos para la app
#
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se indica los       |
#           |                       |  - Representa el        |    campos del modelo   |
#           |        Message        |    mensaje que regresa  |    así como sus pro-   |
#           |                       |    el micro servicio.   |    piedades.           |
#           |                       |                         |                        |
#           +-----------------------+-------------------------+------------------------+
#
#-------------------------------------------------------------------------

from django.db import models
from django.urls import reverse

class Message(models.Model):
    text = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # Clase Meta en donde se indican campos para ordenamiento y el verbose name.
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # Método to String de la clase, la cual es representada por el campo 'name'.
    def __str__(self):
        return self.name

    # Método que regresa la url absoluta del modelo, la cual contiene el campo 'slug'.
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='../../gui/static/media/img', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Clase Meta en donde se indican campos para ordenamiento y el index entre el id y el slug.
    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    # Método to String de la clase, la cual es representada por el campo 'name'.
    def __str__(self):
        return self.name

    # Método que regresa la url absoluta del modelo, la cual contiene los campos 'id' y 'slug'.
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
