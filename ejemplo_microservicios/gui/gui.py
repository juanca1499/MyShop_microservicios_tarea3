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

from flask import Flask, render_template, request
import json, requests
from flask_cors import CORS

app = Flask(__name__,static_url_path='/static/')
CORS(app)

# Se definen las llaves de cada microservicio

key_cart = "a8aa91941a9d46acb9bb4e383f07cc8a"
headers_cart = {"authorization": key_cart}

key_order = "69f999e0beb0413095f73e0e3cf9791d"
header_order = {"authorization": key_order}

key_catalog = "2546998a061a4fb980e6a6e67b179968"
header_catalog = {"authorization": key_catalog}


# Se definen las url para cada micro servicio.
# Se reemplaza el 127.0.0.1 del localhost por host.docker.internal para hacer la conexión
# con los microservicios dentro de los contenedores de Docker.

# Url para el microservicio 1
url_cart = 'http://localhost:8080/cart'
# Url para el microservicio 2
url_order = 'http://host.docker.internal:8080/hello/dart'
# Url para el microservicio 3
url_catalog = 'http://localhost:8000/catalog'


# Método que muestra la página de inicio del sistema
@app.route("/", defaults={'slug': None}, methods=['GET'])
@app.route("/<slug>", methods=['GET'])
def index(slug):
    cart_total = requests.get(url_cart + "/total/abcdefg"headers=headers_cart)
    categories = requests.get(url_catalog + "/category",headers=header_catalog)
    if slug:
        category = requests.get(url_catalog + "/category/" + slug, headers=header_catalog)
        json_category = category.json()
        products = requests.get(url_catalog + "/product/" + slug, headers=header_catalog)
    else:
        products = requests.get(url_catalog + "/product", headers=header_catalog)
        json_category = None

    json_products = products.json()
    json_categories = categories.json() 
    json_result = {'products': json_products,
                   'categories': json_categories,
                   'category': json_category}

    return render_template("catalog/list.html", result=json_result)

@app.route("/category",methods=['GET'])
def categories():
    categories = requests.get(url_catalog + "/category",headers=header_catalog)
    json_categories = categories.json() 
    json_result = {'categories': json_categories}
    return render_template("catalog/list.html", result=json_result)

@app.route("/product/<pk>", methods=['GET'])
def product(pk):
    product = requests.get(url_catalog + "/product/" + pk)
    json_product = product.json()
    category_id = json_product['category']
    category = requests.get(url_catalog + "/category/" + str(category_id))
    json_category = category.json()
    json_result = {'product': json_product,
                   'category' : json_category}

    return render_template("catalog/detail.html", result=json_result)

@app.route("/cart", defaults={'session_id':'abcdefg', 'product_id':None}, methods=['POST'])
@app.route("/cart/<session_id>", defaults={'product_id' : None} , methods=['GET'])
@app.route("/cart/<session_id>/<product_id>", methods=['POST'])
def cart(session_id,product_id): 
    cart_items = None
    # Se agrega un item al carrito. 
    if request.method == "POST":
        print("\n\n\n\n\nENTRE AL POST")
        if product_id==None:
            print(request.form)
            cart_items = requests.post(url_cart + "/items", headers=headers_cart, data = request.form)
        else:
            cart_items = requests.post(url_cart + "/items/"+session_id +"/"+ product_id, headers=headers_cart, data = request.form)
     
    # Se obtiene la lista de items en el carrito
    elif request.method == "GET":
        cart_items = requests.get(url_cart + "/items/" + session_id, headers=headers_cart) 

    cart_info = requests.get(url_cart + "/info/" + session_id, headers=headers_cart)
    json_cart_info = cart_info.json()
    json_cart_items = cart_items.json()
    json_result = {'cart': json_cart_items,
                   'cart_info' : json_cart_info}

    return render_template("cart/detail.html", result=json_result)
    
@app.route("/cart/<session_id>/<product_id>", methods=['GET'])
def delete_cart_item(session_id,product_id):
     # Se solicitó eliminar un item del carrito
    requests.delete(url_cart + "/items/" + session_id + "/" + str(product_id) , headers=headers_cart)
    cart_items = requests.get(url_cart + "/items/" + session_id, headers=headers_cart) 
    cart_info = requests.get(url_cart + "/info/" + session_id, headers=headers_cart)
    json_cart_info = cart_info.json()
    json_cart_items = cart_items.json()
    json_result = {'cart': json_cart_items,
                   'cart_info' : json_cart_info}

    return render_template("cart/detail.html", result=json_result)

@app.route("/items-qty/<str:session_id>")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')