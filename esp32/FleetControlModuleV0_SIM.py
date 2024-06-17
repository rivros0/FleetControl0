import requests
import time
import random

server_url = 'http://test0000.pythonanywhere.com/api/update_location'
vehicle_id = 'VEHICLE002'

while True:
    latitude = random.uniform(38.0, 42.0)
    longitude = random.uniform(17.0, 18.0)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'vehicle_id': vehicle_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    }

    response = requests.post(server_url, data=data)
    print(response.text)
    print(timestamp)
    time.sleep(5)
