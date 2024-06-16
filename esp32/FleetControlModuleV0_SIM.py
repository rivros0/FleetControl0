import requests
import time
import random

server_url = 'http://127.0.0.1:5000/api/update_location'
vehicle_id = 'VEHICLE001'

while True:
    latitude = random.uniform(41.0, 42.0)
    longitude = random.uniform(12.0, 13.0)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'vehicle_id': vehicle_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    }

    response = requests.post(server_url, data=data)
    print(response.text)
    time.sleep(5)
