import requests
import csv
from datetime import datetime

LATACUNGA_LAT = -0.9333
LATACUNGA_LONGITUDE = -78.6167
API_KEY = "507be8cb2b0c6b4ea1bb1ed44165af57"
FILE_NAME = "clima-latacunga-hoy.csv"

def get_weather(lat, lon, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: no se pudo obtener datos de la API. Código de estado: {response.status_code}")
        return None
    
    data = response.json()
    
    if 'main' not in data or 'weather' not in data:
        print("Error: la respuesta de la API no contiene los datos esperados")
        return None

    weather = {
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'weather': data['weather'][0]['description']
    }
    return weather

def write2csv(json_response, csv_filename):
    if json_response is None:
        print("No se escribieron datos debido a un error en la obtención de datos")
        return
    
    file_exists = False
    try:
        with open(csv_filename, 'r') as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['datetime', 'temperature', 'humidity', 'pressure', 'weather'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(json_response)

def process(json_response):
    normalized_dict = json_response
    return normalized_dict

def main():
    print("===== Bienvenido a Latacunga-Clima =====")
    latacunga_weather = get_weather(lat=LATACUNGA_LAT, lon=LATACUNGA_LONGITUDE, api=API_KEY)
    if latacunga_weather:
        processed_data = process(latacunga_weather)
        write2csv(processed_data, FILE_NAME)
    else:
        print("Ciudad no disponible o API KEY no válida")

if __name__ == '__main__':
    main()

