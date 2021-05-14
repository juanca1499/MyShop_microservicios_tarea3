#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: serializers.py
#
# Implementación de Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Jorge Alfonso Solís.
# Version: 1.0.0 Marzo 2021
#
# Descripción:
#
#   En este archivo se definen los serializers de cada modelo de la app
#
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se indica el modelo |
#           |                       |  - Representa el        |    del serializer y    |
#           |   MessageSerializer   |    serializer del       |    los campos a        |
#           |                       |    modelo Message.      |    utilizar.           |
#           |                       |                         |                        |
#           +-----------------------+-------------------------+------------------------+
#
#-------------------------------------------------------------------------

from rest_framework import serializers
from .models import Message, Product, Category

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    