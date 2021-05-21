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

from flask import Flask, render_template, request, redirect, url_for
import json, requests
from flask_cors import CORS

app = Flask(__name__,static_url_path='/static/')
CORS(app)

# Se definen las llaves de cada microservicio

key_cart = "64a36b0f816346028acb48af68c98ed0"
header_cart = {"authorization": key_cart}

key_order = "37ff1871a4ec46da8157b55c28df6de3"
header_order = {"authorization": key_order}

key_catalog = "f479b934654a4e76a42cf5c95adaffc1"
header_catalog = {"authorization": key_catalog}


# Se definen las url para cada micro servicio.
# Se reemplaza el 127.0.0.1 del localhost por host.docker.internal para hacer la conexión
# con los microservicios dentro de los contenedores de Docker.

# Url para el microservicio del carrito
url_cart = 'http://host.docker.internal:8080/cart'
# Url para el microservicio de las órdenes
url_order = 'http://host.docker.internal:8080/order'
# Url para el microservicio del catálogo de productos
url_catalog = 'http://host.docker.internal:8080/catalog'


# Método que muestra la página de inicio del sistema
@app.route("/", defaults={'slug': None}, methods=['GET'])
@app.route("/<slug>", methods=['GET'])
def index(slug):
    json_cart_info, json_cart_items  = get_cart_info()
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
                   'category': json_category,
                    'cart_items': json_cart_items,
                    'cart_info': json_cart_info}

    return render_template("catalog/list.html", result=json_result)

@app.route("/category",methods=['GET'])
def categories():
    json_cart_info, json_cart_items  = get_cart_info()
    categories = requests.get(url_catalog + "/category",headers=header_catalog)
    json_categories = categories.json() 
    json_result = {'categories': json_categories,
                   'cart_items': json_cart_items,
                   'cart_info': json_cart_info}
    return render_template("catalog/list.html", result=json_result)

@app.route("/product/<pk>", methods=['GET'])
def product(pk):
    json_cart_info, json_cart_items  = get_cart_info()
    product = requests.get(url_catalog + "/product/" + pk)
    json_product = product.json()
    category_id = json_product['category']
    category = requests.get(url_catalog + "/category/" + str(category_id))
    json_category = category.json()
    json_result = {'product': json_product,
                   'category' : json_category,
                   'cart_items': json_cart_items,
                   'cart_info': json_cart_info}

    return render_template("catalog/detail.html", result=json_result)

@app.route("/cart", defaults={'session_id':'abcdefg', 'product_id':None}, methods=['POST','GET'])
@app.route("/cart/<session_id>", defaults={'product_id' : None} , methods=['GET'])
@app.route("/cart/<session_id>/<product_id>", methods=['POST'])
def cart(session_id,product_id):
    cart_items = None
    # Se agrega un item al carrito. 
    if request.method == "POST":
        if product_id==None:
            cart_items = requests.post(url_cart + "/items", headers=header_cart, data = request.form)
        else:
            cart_items = requests.post(url_cart + "/items/"+session_id +"/"+ product_id, headers=header_cart, data = request.form)
     
    # Se obtiene la lista de items en el carrito
    elif request.method == "GET":
        cart_items = requests.get(url_cart + "/items/" + session_id, headers=header_cart) 

    cart_info = requests.get(url_cart + "/info/" + session_id, headers=header_cart)
    json_cart_info = cart_info.json()
    json_cart_items = cart_items.json()
    json_result = {'cart_items': json_cart_items,
                   'cart_info' : json_cart_info}

    return render_template("cart/detail.html", result=json_result)
    
@app.route("/cart/<session_id>/<product_id>", methods=['GET'])
def delete_cart_item(session_id,product_id):
     # Se solicitó eliminar un item del carrito
    requests.delete(url_cart + "/items/" + session_id + "/" + str(product_id) , headers=header_cart)
    json_cart_info, json_cart_items  = get_cart_info()
    json_result = {'cart_items': json_cart_items,
                   'cart_info' : json_cart_info}

    return render_template("cart/detail.html", result=json_result)

@app.route("/order/checkout", methods=['GET'])
def order_checkout():
    json_cart_info, json_cart_items  = get_cart_info()
    json_result = {'cart_items': json_cart_items,
                   'cart_info' : json_cart_info}
    return render_template("orders/create.html", result=json_result)

@app.route("/order/place-order", defaults={'id' : None}, methods=['POST'])
@app.route("/order/update/<id>",methods=['POST'])
@app.route("/order/list", defaults={'id' : None}, methods=['GET'])
@app.route("/order/<id>", methods=['GET'])
@app.route("/order/delete/<id>",methods=['GET'])
@app.route("/order/delete-confirm/<id>",methods=['GET'])
def order(id):
    json_cart_info, json_cart_items = get_cart_info()
    orders = requests.get(url_order +  "/order", headers=header_order)
    orders_json = orders.json()
    if request.method == "POST":
        # Se va a crear una nueva orden
        if id==None:
            order = requests.post(url_order + "/order", headers=header_order, data = request.form)
            order_json = order.json()
            order_items = requests.get(url_order + "/order/items/" + str(order_json['id']), headers=header_order)
            cart_delete("abcdefg")
            json_cart_info, json_cart_items = get_cart_info()
            order_items_json = order_items.json()
        
            json_result = {'cart_info': json_cart_info,
                           'cart_items': json_cart_items,
                           'order' : order_json,
                           'cart' : order_items_json}
            return render_template("orders/created.html", result=json_result)
        # Se va a modificar la orden
        else:
            response = requests.post(url_order+"/order/items/"+str(id),headers=header_order, data = request.form)
            # Se eliminaron todos los items de la orden
            if response.status_code == 204:
                orders = requests.get(url_order +  "/order", headers=header_order)
                orders_json = orders.json()
                json_result = {'cart_info': json_cart_info,
                               'cart_items': json_cart_items,
                               'orders': orders_json}
                return render_template("orders/list.html",result=json_result)
           
            # Se canceló un subconjunto de items de la orden
            elif response.status_code == 202:
                order_items= requests.get(url_order + "/order/items/" + str(id), headers=header_order)
                order = requests.get(url_order + "/order/" + str(id) , headers=header_order)
                json_cart_info, json_cart_items = get_cart_info()
                modifiable = get_time_flag(id)
                order_items_json = order_items.json()
                order_json = order.json()
                json_result = {'cart_info': json_cart_info,
                                'cart_items': json_cart_items,
                                'order': order_json,
                                'order_items': order_items_json,
                                'modifiable' : modifiable}
                return render_template("orders/items_list.html",result=json_result)

    elif request.method == "GET":
        if "/order/delete" in str(request.url):
            if "confirm" in str(request.url):
                requests.delete(url_order + '/order/delete/' + str(id), headers=header_order)
                # Se vuelve a hacer la solicitud para que se vean reflejados los cambios.
                orders = requests.get(url_order +  "/order", headers=header_order)
                orders_json = orders.json()
                json_result ={'cart_info': json_cart_info,
                              'cart_items': json_cart_items,
                              'orders': orders_json}
                return render_template("orders/list.html",result=json_result)
            json_result ={'cart_info': json_cart_info,
                        'cart_items': json_cart_items,
                        'id': id}
            return render_template("orders/cancel_order_confirm.html", result=json_result)
        
        # Se va a consultar la lista de ordenes.
        json_result ={'cart_info': json_cart_info,
                      'cart_items': json_cart_items,
                      'orders': orders_json}
        return render_template("orders/list.html",result=json_result)

@app.route("/order/detail/<id>", methods=['GET'])
def order_detail(id):
    json_cart_info, json_cart_items = get_cart_info()
    if request.method == "GET":
        order_items= requests.get(url_order + "/order/items/" + str(id), headers=header_order)
        order = requests.get(url_order + "/order/" + str(id) , headers=header_order)
        modifiable = get_time_flag(id)
        order_items_json = order_items.json()
        order_json = order.json()
        json_result = {'cart_info': json_cart_info,
                        'cart_items': json_cart_items,
                       'order': order_json,
                       'order_items': order_items_json,
                       'modifiable' : modifiable}
        return render_template("orders/items_list.html",result=json_result)

def cart_delete(session_id):
    requests.delete(url_cart + "/delete/" + session_id, headers=header_cart)

def get_time_flag(id):
    flag = requests.get(url_order+ "/order/flag/" +str(id))
    return flag.json()

def get_cart_info(session_id=None):
    cart_items = requests.get(url_cart + "/items/abcdefg", headers=header_cart) 
    cart_info = requests.get(url_cart + "/info/abcdefg", headers=header_cart)
    if cart_info.status_code != 404:
        json_cart_items = cart_items.json()
        json_cart_info = cart_info.json()
        return json_cart_info, json_cart_items
    else:
        return None, None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')