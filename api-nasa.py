from dotenv import load_dotenv
import os, requests, time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

load_dotenv()  
API_KEY = os.getenv('API-KEY')


BASE_URL = f'https://api.nasa.gov/neo/rest/v1/feed'

def get_data(start_date=None, end_date=None):
    '''Obtiene datos de objetos cercanos a la Tierra (NEO) de la API de la NASA para un rango de fechas.
    
    Args:
        start_date (str): La fecha de inicio en formato 'YYYY-MM-DD'. Si no se especifica, se usará la fecha actual.
        end_date (str): La fecha de finalización en formato 'YYYY-MM-DD'. Si no se especifica, se usará la fecha actual.
    
    Returns:
        dict: Un diccionario que contiene datos de NEO. Cada key será un día.
    '''

    if start_date is None:
        start_date = datetime.now().strftime('%Y-%m-%d')
    if end_date is None:
        end_date = start_date
    
    data = {}
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f'{BASE_URL}?api_key={API_KEY}&start_date={date_str}&end_date={date_str}'
        try:
            response = requests.get(url) # Hourly Limit: 1,000 requests per hour
            print(f'Obtenidos datos del {current_date}')
            response.raise_for_status()
            data[date_str] = response.json()['near_earth_objects'][date_str]
        except requests.exceptions.RequestException as e:
            print(f'Error al obtener datos de la API para la fecha {date_str}: {e}')
        
        current_date += timedelta(days=1)
        time.sleep(5)

        #Compruebo que no se ha excedido el límite de solicitudes.
        rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        if rate_limit_remaining <= 0:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            wait_time = reset_time - time.time()
            if wait_time > 0:
                    print(f'Se ha alcanzado el límite de solicitudes. Esperando {wait_time} segundos...')
                    time.sleep(wait_time + 1)
    
    return data


def plot_pie_chart(data):
    '''Representa en un gráfico circular la relación entre NEOs potencialmente peligrosos y no peligrosos.

    Args:
        data (dict): Un diccionario que contiene datos de NEOs. Cada clave representa una fecha en formato 'YYYY-MM-DD' y el valor asociado es una lista de objetos NEO.

    Returns:
        None
    '''    
    if not isinstance(data, dict):
        raise TypeError('El argumento "data" debe ser un diccionario.')

    if not data:
        raise ValueError('El diccionario "data" está vacío. No se pueden determinar las fechas de inicio y fin.')
        
    dangerous_neos = 0
    non_dangerous_neos = 0
    start_date, end_date = get_start_and_end_dates(data)
    
    for date in data:
        for obj in data[date]:
            if obj['is_potentially_hazardous_asteroid']:
                dangerous_neos += 1
            else:
                non_dangerous_neos += 1
    
    proportions = [dangerous_neos, non_dangerous_neos]
    labels = ['Potentially Hazardous NEOs', 'Non-hazardous NEOs']
    colors = ['#ff9999','#66b3ff']

    plt.figure(figsize=(8, 8))
    plt.pie(proportions, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(f'Proportion of Potentially Hazardous and Non-hazardous NEOs ({start_date} to {end_date})')
    plt.axis('equal')  # Asegura que el gráfico es un círculo.
    plt.show()

def plot_neo_data(data):
    """Genera un gráfico de dispersión que muestra la relación entre la distancia mínima
    a la Tierra y la velocidad relativa de los Objetos Cercanos a la Tierra (NEOs), 
    con el tamaño del cuerpo representado por el tamaño de los puntos en el gráfico.

    Args:
        data (dict): Un diccionario donde las claves son fechas y los valores son listas 
        de objetos NEO, cada uno representado por un diccionario con información sobre el NEO.

    Returns:
        None
    """
    if not isinstance(data, dict):
        raise TypeError('El argumento "data" debe ser un diccionario.')

    if not data:
        raise ValueError('El diccionario "data" está vacío. No se pueden determinar las fechas de inicio y fin.')
        
    distances = []
    velocities = []
    sizes = []
    start_date, end_date = get_start_and_end_dates(data)
    
    for date, neos in data.items():
        for neo in neos:
            try:
                miss_distance = float(neo['close_approach_data'][0]['miss_distance']['kilometers'])
                relative_velocity = float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second'])
                # Calculo el tamaño del cuerpo promediando el mínimo y máximo estimados
                estimated_size = (neo['estimated_diameter']['meters']['estimated_diameter_min'] + neo['estimated_diameter']['meters']['estimated_diameter_max']) / 2

                distances.append(miss_distance)
                velocities.append(relative_velocity)
                sizes.append(estimated_size)
            except KeyError as e:
                print(f"Error al procesar los datos: {e}")
                continue

    # Escalar el tamaño del cuerpo para el gráfico de dispersión
    max_size = max(sizes)
    scaled_sizes = [size / max_size * 100 for size in sizes]

    plt.figure(figsize=(10, 6))
    plt.scatter(distances, velocities, s=scaled_sizes, alpha=0.5)

    plt.title('Distancia Mínima a la Tierra vs. Velocidad Relativa de los NEOs')
    plt.title(f'({start_date} to {end_date})', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Distancia Mínima a la Tierra (kilómetros)')
    plt.ylabel('Velocidad Relativa (kilómetros por segundo)')
    plt.legend()

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def get_start_and_end_dates(data):
    '''Obtiene la fecha de inicio y fin de un conjunto de datos representado como un diccionario de fechas.

    Args:
        data (dict): Un diccionario que contiene datos con fechas como claves en formato 'YYYY-MM-DD'.

    Returns:
        tuple: Una tupla que contiene la fecha de inicio y fin del conjunto de datos en formato 'YYYY-MM-DD'.
    '''
    if not isinstance(data, dict):
        raise TypeError('El argumento "data" debe ser un diccionario.')

    if not data:
        raise ValueError('El diccionario "data" está vacío. No se pueden determinar las fechas de inicio y fin.')

    try:
        start_date = min(datetime.strptime(date, '%Y-%m-%d') for date in data.keys())
        end_date = max(datetime.strptime(date, '%Y-%m-%d') for date in data.keys())
    except (KeyError, ValueError) as e:
        raise ValueError('Los datos de fecha en el diccionario "data" no están en el formato esperado.') from e

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

if __name__ == '__main__':
    neo_data = get_data('2024-01-01','2024-01-31')
    plot_pie_chart(neo_data)
    plot_neo_data(neo_data)