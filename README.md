# Ejemplo de Arquitecturas de Microservicios

## Estructura del proyecto

- docs: Directorio que almacena documentos auxiliares para este archivo.
- ejemplo_microservicios: Directorio que almacena el código fuente del programa de ejemplo de Microservicios.

## Prerrequisitos

- Clonar el repositorio:
   ```shell
   $ git clone https://gitlab.com/tareas-arquitectura-de-software-curso/microservicios.git

   $ cd microservicios

   ```

- Instalamos Docker. La manera recomendada para implementar este sistema es utilizando [Docker](https://www.docker.com/), para instalarlo puedes seguir las instrucciones para cada sistema operativo haciendo clic [aquí](https://docs.docker.com/install/). 


- Una vez instalado docker debemos ejecutar los siguientes comandos en la consola para que se descarguen las imágenes necesarias (verificar que el servicio de Docker se encuentra corriendo):

   ```shell
   $ docker pull redis:6

   $ docker pull tykio/tyk-gateway:v3.1.2

   ```


## Despliegue del ejemplo de microservicios

Se deben correr los siguientes comandos en la carpeta raíz del proyecto.


### Creación de la red interna de docker

   ```shell
   $ docker network create --subnet=172.19.0.0/16 --attachable tyk
   ```

### Ejecución del contenedor de redis

   ```shell
   $ docker run -d --name tyk_redis --network tyk --ip 172.19.0.2 redis:6
   ```

### Ejecución del contenedor de tyk

Para el siguiente comando es necesario sustituir la cadena '$(pwd)' por el path del directorio actual (directorio raíz del proyecto).

   ```shell
   $ docker run -d --name tyk_gateway --network tyk --ip 172.19.0.3 -p 8080:8080 -v "$(pwd)/ejemplo_microservicios/tyk-gateway/tyk.standalone.conf:/opt/tyk-gateway/tyk.conf" -v "$(pwd)/ejemplo_microservicios/tyk-gateway/apps:/opt/tyk-gateway/apps" tykio/tyk-gateway:v3.1.2

   ```

### Construcción y ejecución de los microservicios

- Para construir y ejecutar cada uno de los microservicios se deberán realizar los siguientes pasos:

1. Ingresamos a la carpeta que contiene el código fuente del sistema:

   ```shell
   $ cd ejemplo_microservicios

   ```
A partir de este directorio deberemos acceder a la carpeta de cada microservicio para realizar la construcción.


#### Construcción y ejecución del microservicio 1

   ```shell
   $ cd microservice1

   $ docker build -t api-python:1.0 .

   $ docker run -d --name api-python --network tyk --ip 172.19.0.4 api-python:1.0
   
   $ cd ..

   ```


#### Construcción y ejecución del microservicio 2

   ```shell
   $ cd microservice2

   $ docker build -t api-dart:1.0 .

   $ docker run -d --name api-dart --network tyk --ip 172.19.0.5 api-dart:1.0

   $ cd ..

   ```

#### Construcción y ejecución del microservicio 3

   ```shell
   $ cd microservice3

   $ docker build -t api-django:1.0 .

   $ docker run -d --name api-django --network tyk --ip 172.19.0.6 api-django:1.0

   $ cd ..

   ```


### Construcción y ejecución de la GUI

- Antes de construir el contenedor de la interfaz de usuario para probar los microservicios será necesario obtener las llaves de acceso para cada microservicio a través del API Gateway y sustituirlas en el código de la GUI. 


#### Creación de las llaves para el API Gateway

- Para crear las llaves es necesario realizar peticiones tipo POST al servicio de tyk que descargamos anteriormente y que debe estar corriendo en un contenedor de Docker. Cada petición regresará como resultado la información de la llave creada, de la información obtenida lo que nos interesa es el valor de key, el cual debemos guardar pues lo utilizaremos más adelante.

- Las peticiones pueden ser realizadas por medio de alguna herramienta como Postman la cual podemos descargar [aquí](https://www.postman.com/downloads/). Después de descargar e instalar la herramienta, es necesario seguir los siguientes pasos:

    1. De la lista de tipos de peticiones que se encuentra en la parte superior izquierda de la herramienta Postman, seleccionamos POST.

    2. Al lado derecho de esta lista colocamos la url del servicio tyk:

        > http://localhost:8080/tyk/keys

    3. Damos click en la opción 'Headers' e ingresamos la información que se muestra en la siguiente imagen:

    <p align="center">
        <img src="docs/tyk_header.png" width="90%" height="90%">
    </p>

    Nota: Sustituimos la cadena 'tyk-authorization' por la siguiente cadena: 352d20ee67be67f6340b4c0605b044b7.

    Esta información será utilizada para las peticiones de las 3 llaves que se crearán, la información que cambiará será la de la sección de 'Body' como se muestra a continuación.

    4. Para el primer microservicio (Python), en la sección de 'Body' añadiremos la siguiente información en formato JSON como se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_m1.png" width="90%" height="90%">
    </p>

    ```shell
    {
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "2": {
                "api_id": "2",
                "api_name": "Python API"
            }
        }
    }
    ```

    Damos click en el botón 'Send' y si todo funciona de forma correcta, debemos ver algo como lo que se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_respuesta.png" width="100%" height="100%">
    </p>

    Debemos guardar el valor de 'key' pues será utilizado en el código de la GUI para acceder al microservicio.

    5. Para el segundo microservicio (Dart) realizaremos los mismos pasos. En la sección de 'Body' añadiremos la siguiente información en formato JSON como se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_m2.png" width="90%" height="90%">
    </p>

    ```shell
    {
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "3": {
                "api_id": "3",
                "api_name": "Dart API"
            }
        }
    }
    ```

    Damos click en el botón 'Send' y si todo funciona de forma correcta, debemos ver algo como lo que se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_respuesta.png" width="100%" height="100%">
    </p>

    Debemos guardar el valor de 'key' pues será utilizado en el código de la GUI para acceder al microservicio.


    6. Para el tercer microservicio (Django) realizaremos los mismos pasos. En la sección de 'Body' añadiremos la siguiente información en formato JSON como se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_m3.png" width="90%" height="90%">
    </p>

    ```shell
    {
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "4": {
                "api_id": "4",
                "api_name": "Django API"
            }
        }
    }
    ```

    Damos click en el botón 'Send' y si todo funciona de forma correcta, debemos ver algo como lo que se muestra en la imagen:

    <p align="center">
        <img src="docs/tyk_respuesta.png" width="100%" height="100%">
    </p>

    Debemos guardar el valor de 'key' pues será utilizado en el código de la GUI para acceder al microservicio.


- También es posible generar las llaves desde la consola, haciendo uso de curl. 

Nota: Para poder utilizar el comando curl en windows debemos descargar el programa, para esto accedemos al siguiente link:

> https://curl.se/download.html

En el siguiente enlace se encuentra una explicación detallada sobre cómo podemos instalar con éxito curl en nuestra computadora.

> https://www.wikihow.com/Install-Curl-on-Windows

- Ya que tenemos curl instalado, ejecutamos los siguientes comandos:

```shell
$ curl --request POST \
  --url http://localhost:8080/tyk/keys \
  --header 'Content-Type: application/json' \
  --header 'x-tyk-authorization: 352d20ee67be67f6340b4c0605b044b7' \
  --data '{
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "2": {
                "api_id": "2",
                "api_name": "Python API"
            }
        }
    }'
```

```shell
$ curl --request POST \
  --url http://localhost:8080/tyk/keys \
  --header 'Content-Type: application/json' \
  --header 'x-tyk-authorization: 352d20ee67be67f6340b4c0605b044b7' \
  --data '{
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "3": {
                "api_id": "3",
                "api_name": "Dart API"
            }
        }
    }'
```

```shell
$ curl --request POST \
  --url http://localhost:8080/tyk/keys \
  --header 'Content-Type: application/json' \
  --header 'x-tyk-authorization: 352d20ee67be67f6340b4c0605b044b7' \
  --data '{
        "rate": 1000,
        "per": 1,
        "expires": 0,
        "quota_max": -1,
        "quota_renews": 1458667309,
        "quota_remaining": -1,
        "quota_renewal_rate": 60,
        "access_rights": {
            "4": {
                "api_id": "4",
                "api_name": "Django API"
            }
        }
    }'
```

- Si se ejecutaron con éxito, de cada comando se obtuvo una salida como la que se muestra en la siguiente imagen:

    <p align="center">
        <img src="docs/curl_key_tyk.png" width="90%" height="90%">
    </p>

    Es importante recordar que debemos guardar el valor de 'key' pues será utilizado en el código de la GUI para acceder a cada microservicio.


- Una vez que tengamos la llave para cada uno de los microservicios procederemos a sustituirlas en el archivo ejemplo_microservicios/gui/gui.py de la siguiente manera:

    1. En la línea número 33, remover el texto <microservice1_key> y reemplazarlo por la llave generada para la Python API.

    2. En la línea número 36, remover el texto <microservice2_key> y reemplazarlo por la llave generada para la Dart API.

    3. En la línea número 39, remover el texto <microservice3_key> y reemplazarlo por la llave generada para la Django API.

#### Construcción del contenedor de la GUI

- Ahora es momento de construir el contenedor de la GUI, para lograrlo ejecutamos los siguientes comandos desde el directorio 'ejemplo_microservicios':

   ```shell
   $ cd gui

   $ docker build -t gui:1.0 .

   ```

#### Ejecución del contenedor de la GUI

- Para levantar el contenedor de la GUI ejecutamos el siguiente comando:

   ```shell
   $ docker run -d --name gui -p 5000:5000 gui:1.0

   ```

- Si todo se ejecutó con éxito podemos corroborar que nuestros contenedores se encuentran corriendo ejecutando el siguiente comando:

    ```shell
    $ docker ps

    ```
    Este comando nos mostrará los contenedores que se encuentran corriendo, en la columna Status, debemos observar la palabra UP en los contenedores gui, api-python, api-dart, api-django, redis y tykio/tyk-gateway.

- Ya que confirmamos que nuestros contenedores se encuentran corriendo podremos ingresar a nuestro navegador y verificar que el sistema de ejemplo para probar los microservicios se encuentra funcionando correctamente, ingresamos a la siguiente url: 

> http://localhost:5000/

- Si todo funcionó correctamente debemos poder ver la siguiente interfaz, en donde podremos probar el funcionamiento de los microservicios:

    <p align="center">
        <img src="docs/gui_microservicios.png" width="90%" height="90%">
    </p>


## Desarrollo

### Microservicio 1 - Python

- Para el desarrollo del microservicio 1 es necesario contar con python 3.9 o superior y pip3 (las pruebas fueron realizadas con la versión 3.9.1). Se recomienda utilizar [pyenv](https://github.com/pyenv/pyenv) como manejador de versiones de python; una vez instalado se pueden seguir los siguientes comandos para instalar la versión deseada de python, esto hay que realizarlo en la raíz del repositorio:

   ```shell
   $ pyenv install 3.9.1
   $ pyenv local 3.9.1
   ```

- Crear un ambiente virtual para manejar las dependencias ejecutando:
   
   ```shell
   $ python3 -m venv venv
   ```

   en Windows:

   ```shell
   $ python3 -m venv venv
   ```

   si no funciona el comando anterior, ejecutar el siguiente:
   ```shell
   $ py -3 -m venv venv
   ```

   Esto creará una carpeta llamada "venv" que representa nuestro ambiente virtual y donde instalaremos todas las dependencias.

- Activamos el ambiente virtual:
   ```shell
   $ source venv/bin/activate
   ```

   o en Windows:
   ```shell
   $ venv\Scripts\activate
   ```

- Instalamos las dependencias del microservicio ejecutando:
   ```shell
   (venv)$ cd microservice1

   (venv)$ pip3 install -r requirements.txt 
   ```

   Los paquetes que se instalarán son los siguientes:

    Paquete      |  Versión  | 
   --------------|-----------|
    falcon       |   2.0.0   |
    falcon-cors  |   1.1.7   |
    gunicorn     |  20.0.4   |
    waitress     |   2.0.0   |


#### Ejecución

- Dentro del directorio del microservicio (microservice1) ejecutamos la aplicación en Linux:

   ```shell
   (venv)$ gunicorn hello_python.app --bind 0.0.0.0:8000

   ```

- En Windows:

   ```shell
   (venv)$ waitress-serve --port=8000 hello_python.app:api

   ```

- Para probar el microservicio podemos hacer la petición GET desde Postman como se muestra en la siguiente imagen:

    <p align="center">
        <img src="docs/prueba_m1.png" width="90%" height="90%">
    </p>

Nota: Recordar que en este caso estamos probando el microservicio sin la ayuda del contenedor de Docker ni el servicio de tyk, por lo que no nos pide ninguna llave. Esta ejecución se recomienda realizarla solamente durante desarrollo.

### Microservicio 2 - Dart

- Para el desarrollo del microservicio 2 es necesario contar con Dart 2.10.5 o superior.

#### Ejecución

- Entramos a la carpeta del microservicio:
   ```shell
   (venv)$ cd microservice2
   ```

- Es necesario tomar en cuenta que la aplicación Dart se encuentra configurada con el host y el puerto para funcionar en el contenedor de Docker. Si se desea ejecutar la aplicación en tiempo de desarrollo fuera del contenedor de Docker, es necesario cambiar el host por '0.0.0.0' y ejecutar el siguiente comando:

   ```shell
   (venv)$ dart hello_dart/app.dart 

   ```

- Para probar el microservicio podemos hacer la petición GET desde Postman como se muestra en la siguiente imagen:

    <p align="center">
        <img src="docs/prueba_m2.png" width="90%" height="90%">
    </p>

Nota: Recordar que en este caso estamos probando el microservicio sin la ayuda del contenedor de Docker ni el servicio de tyk, por lo que no nos pide ninguna llave. Esta ejecución se recomienda realizarla solamente durante desarrollo.


### Microservicio 3 - Django

- Para el desarrollo del microservicio 3 es necesario contar con python 3.9 o superior y pip3 (las pruebas fueron realizadas con la versión 3.9.1). Se recomienda utilizar [pyenv](https://github.com/pyenv/pyenv) como manejador de versiones de python; una vez instalado se pueden seguir los siguientes comandos para instalar la versión deseada de python, esto hay que realizarlo en la raíz del repositorio:

   ```shell
   $ pyenv install 3.9.1
   $ pyenv local 3.9.1
   ```

- Crear un ambiente virtual para manejar las dependencias ejecutando:
   
   ```shell
   $ python3 -m venv venv
   ```

   en Windows:

   ```shell
   $ python3 -m venv venv
   ```

   si no funciona el comando anterior, ejecutar el siguiente:
   ```shell
   $ py -3 -m venv venv
   ```

   Esto creará una carpeta llamada "venv" que representa nuestro ambiente virtual y donde instalaremos todas las dependencias.

- Activamos el ambiente virtual:
   ```shell
   $ source venv/bin/activate
   ```

   o en Windows:
   ```shell
   $ venv\Scripts\activate
   ```

- Instalamos las dependencias del microservicio ejecutando:
   ```shell
    (venv)$ cd microservice3 

    (venv)$ pip3 install -r requirements.txt 
   ```

   Los paquetes que se instalarán son los siguientes:

    Paquete              |  Versión  | 
   ----------------------|-----------|
    django               |   3.1.7   |
    djangorestframework  |   3.12.2  |
    django-cors-headers  |   3.5.0   |
    Pillow               |   8.1.1   |
    gunicorn             |  20.0.4   |


#### Ejecución

- Dentro del directorio del microservicio (microservice3) ejecutamos el siguiente comando:
   ```shell
   (venv)$ python manage.py runserver 0.0.0.0:8000 

   ```

- Para probar el microservicio podemos hacer la petición GET desde Postman como se muestra en la siguiente imagen:

    <p align="center">
        <img src="docs/prueba_m3.png" width="90%" height="90%">
    </p>

Nota: Recordar que en este caso estamos probando el microservicio sin la ayuda del contenedor de Docker ni el servicio de tyk, por lo que no nos pide ninguna llave. Esta ejecución se recomienda realizarla solamente durante desarrollo.

### GUI - Python

- Para el desarrollo de la GUI es necesario contar con python 3.9 o superior y pip3 (las pruebas fueron realizadas con la versión 3.9.1). Se recomienda utilizar [pyenv](https://github.com/pyenv/pyenv) como manejador de versiones de python; una vez instalado se pueden seguir los siguientes comandos para instalar la versión deseada de python, esto hay que realizarlo en la raíz del repositorio:

   ```shell
   $ pyenv install 3.9.1
   $ pyenv local 3.9.1
   ```

- Crear un ambiente virtual para manejar las dependencias ejecutando:
   
   ```shell
   $ python3 -m venv venv
   ```

   en Windows:

   ```shell
   $ python3 -m venv venv
   ```

   si no funciona el comando anterior, ejecutar el siguiente:
   ```shell
   $ py -3 -m venv venv
   ```

   Esto creará una carpeta llamada "venv" que representa nuestro ambiente virtual y donde instalaremos todas las dependencias.

- Activamos el ambiente virtual:
   ```shell
   $ source venv/bin/activate
   ```

   o en Windows:
   ```shell
   $ venv\Scripts\activate
   ```

- Instalamos las dependencias de la GUI ejecutando:
   ```shell
   (venv)$ cd gui

   (venv)$ pip3 install -r requirements.txt 

   ```

   Los paquetes que se instalarán son los siguientes:

    Paquete      |  Versión  | 
   --------------|-----------|
    Flask        |   1.1.2   |
    Flask-Cors   |   3.0.9   |
    requests     |   2.25.0  |
    Pillow       |   8.1.1   |
    gunicorn     |  20.0.4   |


#### Ejecución

- Dentro del directorio de la GUI ejecutamos el siguiente comando:
   ```shell
   (venv)$ python gui.py

   ```

- Para probar la GUI, ingresamos a la url http://localhost:5000/ en el navegador, lo podemos hacer dando click [aquí](http://localhost:5000/) y debemos poder ver algo parecido a la siguiente imagen:

    <p align="center">
        <img src="docs/prueba_gui.png" width="90%" height="90%">
    </p>


## Despliege

- Cuando se haya finalizado el desarrollo de cada microservicio o de la GUI, simplemente se deben correr los siguientes comandos en la carpeta correspondiente y se podrá verificar el funcionamiento del programa.

Es importante verificar que los contenedores se encuentran detenidos para asegurar que la construcción tenga éxito.


### Construir y correr el microservicio 1

- Ejecutamos los siguientes comandos para construir y ejecutar el contenedor de Docker:

   ```shell
   $ cd microservice1

   $ docker build -t api-python:1.0 .

   $ docker run -d --name api-python --network tyk --ip 172.19.0.4 api-python:1.0

   ```

### Construir y correr el microservicio 2

- Ejecutamos los siguientes comandos para construir y ejecutar el contenedor de Docker:

   ```shell
   $ cd microservice2

   $ docker build -t api-dart:1.0 .

   $ docker run -d --name api-dart --network tyk --ip 172.19.0.5 api-dart:1.0

   ```

### Construir y correr el microservicio 3

- Ejecutamos los siguientes comandos para construir y ejecutar el contenedor de Docker:

   ```shell
   $ cd microservice3

   $ docker build -t api-django:1.0 .

   $ docker run -d --name api-django --network tyk --ip 172.19.0.6 api-django:1.0

   ```


### Construir y correr la GUI

- Ejecutamos los siguientes comandos para construir y ejecutar el contenedor de Docker:

   ```shell
   $ cd gui

   $ docker build -t gui:1.0 .

   $ docker run -d --name gui -p 5000:5000 gui:1.0

   ```

- Si todo se ejecutó con éxito podemos corroborar que nuestros contenedores se encuentran corriendo ejecutando el siguiente comando:

    ```shell
    $ docker ps

    ```
    Este comando nos mostrará los contenedores que se encuentran corriendo, en la columna Status, debemos observar la palabra UP en los contenedores gui, api-python, api-dart, api-django, redis y tykio/tyk-gateway.

- Ya que confirmamos que nuestros contenedores se encuentran corriendo podremos ingresar a nuestro navegador y verificar que el sistema de ejemplo para probar los microservicios se encuentra funcionando correctamente, ingresamos a la siguiente url: 

> http://localhost:5000/



## Comandos Docker

- Para corroborar que nuestros contenedores se encuentran corriendo podemos ejecutar el siguiente comando:

    ```shell
    $ docker ps

    ```
    Este comando nos mostrará los contenedores que se encuentran corriendo, en la columna Status, debemos observar la palabra UP en el contenedor. 

- Cada vez que realicemos cambios en nuestra aplicación se recomienda reiniciar el contenedor; para esto podemos utilizar el siguiente comando:

    ```shell
    $ docker restart <container_name>

    ```

- Finalmente, si deseamos detener alguno de nuestros contenedores, ejecutamos el siguiente comando:

    ```shell
    $  docker stop <container_name>
    ```

## Versión

1.0.0 - Marzo 2021

## Autores

* **Perla Velasco**
* **Jorge Alfonso Solís**