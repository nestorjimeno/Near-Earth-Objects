# NASA NEO API Data Fetcher

Este script Python se utiliza para obtener datos sobre objetos cercanos a la Tierra (NEO, por sus siglas en inglés) de la NASA utilizando su API.

## Requisitos

- Python 3.x
- `dotenv` (instalable a través de `pip install python-dotenv`)
- Una clave de API de la NASA NEO (se puede obtener [aquí](https://api.nasa.gov/))

## Configuración

1. Clona este repositorio o copia el contenido del script a tu entorno.
2. Crea un archivo `.env` en el mismo directorio que el script.
3. Dentro del archivo `.env`, agrega tu clave de API de la NASA NEO de la siguiente manera:
    ```
    API_KEY=TU_CLAVE_DE_API
    ```
4. Guarda el archivo `.env`.

## Uso

1. Ejecuta el script Python.
2. Los datos sobre objetos cercanos a la Tierra para la fecha especificada (o por defecto, la fecha actual) se recuperarán de la API de la NASA NEO y se imprimirán en la consola.

## Ejemplo

```python
python nasa_neo_fetcher.py
```

## Licencia

Este proyecto está bajo la licencia MIT.