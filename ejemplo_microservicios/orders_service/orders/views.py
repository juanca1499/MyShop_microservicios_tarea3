from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.core.mail import send_mail
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from django.conf import settings
from .models import OrderItem, Order
from .serializers import OrderSerializer, OrderItemSerializer
import decimal
import json
import pytz
import time

class OrderViewSet(viewsets.ViewSet):
    # Método que se accede por la URL /order
    def list(self, request):
        # Se obtiene la lista de ordenes
        orders = Order.objects.all()
        # Se crea el serializer y se envía como response
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def items_list(self, request, pk):
        # Se obtiene la orden con el id recibido
        order = get_object_or_404(Order, id=pk)
        # Se obtienen todos los items registrados en la base de datos
        order_items = OrderItem.objects.all()
        # Se filtran los items para obtener los que pertenecen a la orden solicitada
        order_items = order_items.filter(order=order)
        # Se crea el serializer
        serializer = OrderItemSerializer(order_items, many=True)
        # Se envía la <respuesta a la solicitud
        return Response(serializer.data) 

    # Método que se accede por la URL /orders
    def create(self, request):
        #Extraemos los items del carrito
        cart_items = request.data['cart_items']
        cart_items = cart_items.replace("'", '"')
        cart_items_json = json.loads(cart_items)
        #Exraemos los datos del usuario para crear una nueva orden
        nueva_orden= Order()
        nueva_orden.first_name=request.data['first_name']
        nueva_orden.last_name=request.data['last_name']
        nueva_orden.email=request.data['email']
        nueva_orden.address=request.data['address']
        nueva_orden.postal_code=request.data['postal_code']
        nueva_orden.city=request.data['city']
        nueva_orden.total=request.data['order_total']
        # Guardamos la nueva orden
        nueva_orden.save()
        cart = []
        # Creamos los items de la orden
        for item in cart_items_json:
            nuevo_item = OrderItem()
            nuevo_item.order = nueva_orden
            nuevo_item.product_id = item['product_id']
            nuevo_item.name = item['name']
            nuevo_item.image = item['image']
            nuevo_item.unit_price = item['unit_price']
            nuevo_item.quantity = item['quantity']
            nuevo_item.price = item['price']
            nuevo_item.save()
            cart.append(nuevo_item)
        
        # Se envía el correo de confirmación de la órden
        self.send(nueva_orden,cart)
        # Se crea el serializer 
        serializer = OrderSerializer(nueva_orden)
        # Se envía la respuesta de la solicitud
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Método que se accede por la URL /order/<str:pk>
    def retrieve(self, request, pk):
        # Se obtiene la orden con ayuda del pk recibido
        order = Order.objects.get(id=pk)
        # Se crea el serializer
        serializer = OrderSerializer(order)
        # Se envía la respuesta a la solicitud
        return Response(serializer.data)

    # Método que se accede por la URL /order/<str:pk>
    def update(self, request, pk): 
        # Se obtiene la orden con ayuda del pk recibido
        order = Order.objects.get(id=pk)
        # Se crea el serializer con los datos recibidos
        serializer = OrderSerializer(instance=order, data=request.data)
        # Se verifica si el serializer es válido
        serializer.is_valid(raise_exception=True)
        # Se guarda el serializer
        serializer.save()
        # Se envía la respuesta a la solicitud
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # Método que se accede por la URL /orders/<str:pk>
    def destroy(self, request, pk=None):
        # Se obtiene la orden con ayuda del pk recibido
        order = Order.objects.get(id=pk)
        notas=['cancelled','were contained','cancellation']
        # Se envía el correo con los datos de la cancelación.
        self.confirm(order.id,notas)
        # Se procede a eliminar la orden
        order.delete()
        # Se envía la respuesta a la solicitud
        return Response(status=status.HTTP_204_NO_CONTENT)

    def send(self, order, cart):
        # Se crea el subject del correo.
        subject = 'Order nr. {}'.format(order.id)

        # Se define el mensaje a enviar.
        message = 'Dear {},\n\nYou have successfully placed an order. The id of your order is {}.\n\n\n'.format(order.first_name,order.id)
        message_part2 = 'Your order: \n\n'
        mesagges = []

        for item in cart:
            msg = str(item.quantity) + 'x '+ item.name +'  $'+ str(item.price)+ '\n'
            mesagges.append(msg)
        
        message_part3 = ' '.join(mesagges)
        message_part4 = '\n\n\n Total: $'+ str(order.total)
        body = message + message_part2 + message_part3 + message_part4

        # Se envía el correo.
        send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

    def time_verify(self, request, pk):
        order = Order.objects.get(id=pk)    #   Obtener id de la orden que se quiere consultar 

        #   Variable que indica si ya han pasado o no las 24 horas desde que se confirmó la orden. 
        # Flag igual a True indica que aún puede modificarse la orden, dado que no han pasado 24 horas.
        # Flag igual a False indica que ya no puede modificarse la orden, dado que ya pasaron 24 horas.
        flag = True  

        todays_date = datetime.now() # Obtener fecha y hora del sistema (esta variable no considera la zona horaria)
        timezone = pytz.timezone(settings.TIME_ZONE) # Se crea una zona horaria en formato tzfile basada en la zona horaria 
                                                    # definida en el archivo settings del proyecto.

        todays_date_wo = timezone.localize(todays_date) # Se asigna la zona horaria 'timezone' a la fecha del sistema 
        takeaway_hours = todays_date_wo - timedelta(hours=24) # Se obtienen la fecha y hora exactas 24 antes de la fecha actual.
        
        # Se obtiene la fecha en la que fue confirmada la orden y se transforma a la zona horaria del sistema local (provista en el archivo settings). 
        order_date = order.created.replace(tzinfo=pytz.utc)
        order_date = order_date.astimezone(timezone)

        # ¿Ya pasaron 24 horas desde la confirmación del pedido?:
        if (takeaway_hours > order_date):
            flag = False
        
        return Response(flag)

    def confirm(self, order_id, notas):
        print("\n\n\n\n")
        print("******************** ENTRO AL CONFIRM ********************")
        # Se obtiene la información de la orden.
        order = Order.objects.get(id=order_id)

        # Se crea el subject del correo.
        subject = 'Order nr. {}'.format(order.id)

        # Se define el mensaje a enviar.
        message = 'Dear {},\n\nYou have successfully {} your order. The number of your {} order is {}.\n\n\n'.format(order.first_name,notas[0],notas[0],order.id)
        message_part2 = 'The following products {} in your order: \n\n'.format(notas[1])
        mesagges = []

        order_items = []
        order_items = OrderItem.objects.filter(order=order_id)

        for item in order_items:
            msg = str(item.quantity) + 'x '+ str(item.name) +'  $'+ str(item.price)+ '\n'
            mesagges.append(msg)
        
        message_part3 = ' '.join(mesagges)
        message_part4 = '\n\n\n Total: $'+ str(order.total)
        message_part5 = '\n\n\n Date of '+ notas[2] +' : ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        body = message + message_part2 + message_part3 + message_part4 + message_part5

        # Se envía el correo.
        send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

    def update_confirm(self, order_id):
        # Se obtiene la información de la orden.
        order = Order.objects.get(id=order_id)

        # Se crea el subject del correo.
        subject = 'Order nr. {}'.format(order.id)

        # Se define el mensaje a enviar.
        message = 'Dear {},\n\nYou have successfully updated your order. The number of your updated order is {}.\n'.format(order.first_name,order.id)

        message_part2 = '\n\n Date of update : ' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        body = message + message_part2

        # Se envía el correo.
        send_mail(subject, body, 'pruebas.jogglez@gmail.com', [order.email], fail_silently=False)

    def update_order(self, request, pk):
        if request.method == "POST":
            # Se extrae la lita de OrderItems seleccionadas.
            ids_to_delete = []
            for key in request.data:
                ids_to_delete.append(request.data[key])

            # Validamos que se haya seleccionado por lo menos un OrderItem.
            if len(ids_to_delete) > 0:
                # Se consulan los OrderItem que tiene que tiene la Order.
                items_in_order = OrderItem.objects.filter(order=pk)
                # Si se seleccionaron todos los productos de la orden, 
                # entonces se procede a una cancelación total.
                if len(ids_to_delete) == len(items_in_order):
                    return self.destroy(request,pk)
                # De lo contrario, se procede a la cancelación parcial.
                else:
                    order = get_object_or_404(Order, id=pk)
                    for item_id in ids_to_delete:
                        order_item = OrderItem.objects.get(id=item_id)
                        # Se resta el monto de los productos cancelados de la orden
                        order.total = order.total - order_item.price
                        order_item.delete()     
                    order.save()
                    self.update_confirm(pk)
                    self.confirm(pk,['modified','are still','modification'])
    
        return Response(status=status.HTTP_202_ACCEPTED)

    
        