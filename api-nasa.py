from dotenv import load_dotenv
import os, requests
from datetime import datetime

load_dotenv()  
API_KEY = os.getenv('API-KEY')


URL = f'https://api.nasa.gov/neo/rest/v1/feed?api_key={API_KEY}&start_date='

def get_data(date='2024-04-01'):
    response = requests.get(URL + date)
    response.raise_for_status()
    return response.json()['near_earth_objects']

data=get_data()

