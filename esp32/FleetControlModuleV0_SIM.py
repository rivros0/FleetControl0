import requests
import time
import random

server_url = 'http://test0000.pythonanywhere.com/api/update_location'
vehicle_ids = ['VEHICLE001', 'VEHICLE002', 'VEHICLE003']

while True:
    for vehicle_id in vehicle_ids:
        latitude = random.uniform(38.0, 42.0)
        longitude = random.uniform(17.0, 18.0)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'vehicle_id': vehicle_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp
        }

        try:
            response = requests.post(server_url, data=data)
            response.raise_for_status()  # Raise an error for bad status codes
            print(f"Data sent for {vehicle_id}: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data for {vehicle_id}: {e}")

    time.sleep(5)
