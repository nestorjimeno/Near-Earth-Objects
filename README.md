# Visualización de Objetos Cercanos a la Tierra (NEOs) con Python y la API de la NASA

## Introducción
¿Es realmente posible que tengamos un "encuentro" con un meteorito? Los Objetos Cercanos a la Tierra o Near Earth Objects (NEO), son cuerpos que orbitan cerca de nuestro planeta, algunos de los cuales pueden llegar a suponer una amenaza real. En este proyecto, vamos a ver cómo utilizar Python y la API abierta de la NASA para obtener información sobre ellos: conocer su tamaño, su velocidad y su proximidad a la Tierra.

La NASA proporciona una enorme cantidad de información pública a través de sus APIs. La que utilizamos en este proyecto es NeoWs (Near Earth Object Web Service), un servicio web RESTful para información sobre asteroides cercanos a la Tierra. Con NeoWs, un usuario puede buscar asteroides basados en su fecha de aproximación más cercana a la Tierra, buscar un asteroide específico con su identificador de pequeño cuerpo de la NASA JPL, así como explorar el conjunto de datos en general.

## Cómo usar
Para ejecutar este proyecto, primero asegúrate de tener Python instalado en tu sistema. Luego, sigue estos pasos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando `pip install -r requirements.txt`.
3. Crea un archivo `.env` en el directorio raíz del proyecto y añade tu API Key de la NASA siguiendo el formato `API_KEY=TU_API_KEY`.
4. Ejecuta el script principal `api-nasa.py` con el comando `python api-nasa.py`.

## Funcionalidades
Este proyecto consta de las siguientes funcionalidades principales:

### Obtención de datos de la NASA
La función `get_data()` se encarga de obtener datos de objetos cercanos a la Tierra (NEO) de la API de la NASA para un rango de fechas especificado.

### Visualización de datos en gráfico circular
La función `plot_pie_chart(data)` representa en un gráfico circular la relación entre NEOs potencialmente peligrosos y no peligrosos.

### Visualización de datos en gráfico de dispersión
La función `plot_neo_data(data)` genera un gráfico de dispersión que muestra la relación entre la distancia mínima a la Tierra y la velocidad relativa de los Objetos Cercanos a la Tierra (NEOs), con el tamaño del cuerpo representado por el tamaño de los puntos en el gráfico.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, siéntete libre de hacer fork y enviar un pull request con tus sugerencias.

## Autor
Este proyecto fue desarrollado por Néstor Jimeno ([GitHub](https://github.com/nestorjimeno) y [LinkedIn](https://www.linkedin.com/in/nestorjimeno/)).
