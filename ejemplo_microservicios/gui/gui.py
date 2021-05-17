# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: gui.py
# Implementación de Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Jorge Alfonso Solís.
# Version: 1.0 Marzo 2021
# Descripción:
#
#   Este archivo define la interfaz gráfica del usuario. Recibe un parámetro que define el 
#   Microservicio que se desea utilizar.
#   
#                                             gui.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Porporcionar la in-  | - Consume servicios    |
#           |          GUI          |    terfaz gráfica con la|   para proporcionar    |
#           |                       |    que el usuario hará  |   información al       |
#           |                       |    uso del sistema.     |   usuario.             |
#           +-----------------------+-------------------------+------------------------+
#

from flask import Flask, render_template
import json, requests
from flask_cors import CORS

app = Flask(__name__,static_url_path='/static/')
CORS(app)

# Se definen las llaves de cada microservicio

key_m1 = "a8aa91941a9d46acb9bb4e383f07cc8a"
headers_m1 = {"authorization": key_m1}

key_m2 = "69f999e0beb0413095f73e0e3cf9791d"
header_m2 = {"authorization": key_m2}

key_m3 = "2546998a061a4fb980e6a6e67b179968"
header_m3 = {"authorization": key_m3}


# Se definen las url para cada micro servicio.
# Se reemplaza el 127.0.0.1 del localhost por host.docker.internal para hacer la conexión
# con los microservicios dentro de los contenedores de Docker.

# Url para el microservicio 1
url_microservice1 = 'http://localhost:8080/cart'
# Url para el microservicio 2
url_microservice2 = 'http://host.docker.internal:8080/hello/dart'
# Url para el microservicio 3
url_microservice3 = 'http://localhost:8000/catalog'


# Método que muestra la página de inicio del sistema
@app.route("/", defaults={'slug': None}, methods=['GET'])
@app.route("/<slug>", methods=['GET'])
def index(slug):
    categories = requests.get(url_microservice3 + "/category",headers=header_m3)
    if slug:
        category = requests.get(url_microservice3 + "/category/" + slug, headers=header_m3)
        json_category = category.json()
        products = requests.get(url_microservice3 + "/product/" + slug, headers=header_m3)
    else:
        products = requests.get(url_microservice3 + "/product", headers=header_m3)
        json_category = None

    json_products = products.json()
    json_categories = categories.json() 
    json_result = {'products': json_products,
                   'categories': json_categories,
                   'category': json_category}

    return render_template("catalog/list.html", result=json_result)

@app.route("/category",methods=['GET'])
def categories():
    categories = requests.get(url_microservice3 + "/category",headers=header_m3)
    json_categories = categories.json() 
    json_result = {'categories': json_categories}
    return render_template("catalog/list.html", result=json_result)

@app.route("/product/<pk>", methods=['GET'])
def product(pk):
    product = requests.get(url_microservice3 + "/product/" + pk)
    json_product = product.json()
    category_id = json_product['category']
    category = requests.get(url_microservice3 + "/category/" + str(category_id))
    json_category = category.json()
    json_result = {'product': json_product,
                   'category' : json_category}

    return render_template("catalog/detail.html", result=json_result)

@app.route("/<api>", methods=['GET'])
def other(api):
    
    # Se verifica si se recibió la variable api
    if api:

        if int(api) == 1:
            # Se llama al microservicio enviando como parámetro la url y el header
            ms1 = requests.get(url_microservice1, headers=headers_m1)
            # Se convierte la respuesta a json
            json = ms1.json()
            # Se crea el json que será enviado al template
            json_result = {'ms1': json}
        elif int(api) == 2:
            # Se llama al microservicio enviando como parámetro la url y el header
            ms2 = requests.get(url_microservice2, headers=header_m2)
            # Se convierte la respuesta a json
            json = ms2.json()
            # Se crea el json que será enviado al template
            json_result = {'ms2': json}
        elif int(api) == 3:
            # Se llama al microservicio enviando como parámetro la url y el header 
            ms3 = requests.get(url_microservice3, headers=header_m3)
            # Se convierte la respuesta a json
            json = ms3.json()
            # Se crea el json que será enviado al template
            json_result = {'ms3': json}
            return render_template("catalog/list.html", result=json_result)
        
        #return render_template("index.html", result=json_result)
    
    # Si no se reciben datos, se muestra la lista de productos (vista inicial)
    else:
        pass
        #categories = requests.get(url_microservice3 + "/category",headers=header_m3)
        #json_categories = categories.json() 

# @app.route("add/<str:pk>",methods=[GET])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')