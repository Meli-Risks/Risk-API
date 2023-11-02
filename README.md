# Risk API

## Despliegue Local

1. Primero, clona el repositorio en tu máquina local:

    ``
    git clone <url_del_repositorio>
    ``
2. Navega hasta el directorio del proyecto:

    ``
    cd <nombre_del_directorio_del_proyecto>
    ``

3. Crea un entorno virtual e instala las dependencias:

    ``
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ``

4. Ejecuta la aplicación:

    ``
    FLASK_APP=run.py FLASK_ENV=development python -m flask run
    ``

5. La aplicación Flask ahora debería estar desplegada en http://localhost:5000.

## Despliegue con Docker

Asegúrese de estar en el directorio del proyecto donde se encuentra el Dockerfile.

1. Construye la imagen de Docker:

    ``
    docker build -t <nombre_de_la_imagen> .
    ``

2. Corre el contenedor de Docker:

    ``
    docker run -p 5000:5000 <nombre_de_la_imagen>
    ``

3. Ahora, la aplicación Flask debería estar desplegada en http://localhost:5000.

Por favor, reemplaza <url_del_repositorio>, <nombre_del_directorio_del_proyecto> y <nombre_de_la_imagen> con los valores correspondientes a tu proyecto. 
