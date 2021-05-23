# Microservice catalog: django - MyShop

Esta carpeta contiene el código fuente del Microservice catálogo para el sistema MyShop. El microservicio fue desarrollada utilizando el lenguaje de programación python y el framework django.

## Estructura del Directorio

- catalog: Directorio que almacena el código fuente de la aplicación catálogo.
- catalog_service: Directorio que almacena el código fuente de la aplicación en general.
- db.sqlite3: Archivo de la base de datos del microservicio.
- Dockerfile: Archivo que contiene las configuraciones necesarias para el despliegue del microservicio en Docker.
- gunicorn.conf: Archivo que contiene las configuraciones necesarias para el despliegue del microservicio.
- manage.py: Archivo para el manejo del sistema desarrollado con el Framework django.
- requirements.txt: Archivo que contiene las dependencias de la aplicación.

### Construcción y ejecución del microservicio catálogo

- Estas son algunas consideraciones a tomar en cuenta para construir y ejecutar el contenedor del microservicio catálogo. Si ya se llevaron acabo estos pasos que son mencionados también en el archivo README.md de la carpeta raíz, por favor omitirlos.

   ```shell
   $ cd catalog_service

   $ docker build -t api-catalog:1.0 .

   $ docker run -d --name api-catalog --network tyk --ip 172.15.0.4 api-catalog:1.0
   
   $ cd ..
   ```

   En Linux:

   ```shell
   $ cd catalog_service

   $ sudo docker build -t api-catalog:1.0 .

   $ sudo docker run -d --name api-catalog --network tyk --ip 172.15.0.4 api-catalog:1.0
   
   $ cd ..
   ```

## Versión

2.0.0 - Mayo 2021

## Autores

* **Perla Velasco**
* **Jorge Alfonso Solís**
* **Alejandro Carrillo Villegas**
* **César Gabriel Díaz Curiel**
* **Juan Carlos García Murillo**
* **Josué Guillermo González Pinedo**
* **José Germán González Rodarte**