import requests
import time
import random

server_url = 'http://test0000.pythonanywhere.com/api/update_location'
vehicle_ids = ['VEHICLE001','VEHICLE002','VEHICLE003']

while True:
    latitude = random.uniform(38.0, 42.0)
    longitude = random.uniform(17.0, 18.0)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    for i in range(len(vehicle_ids)):
        data = {
            'vehicle_id': vehicle_ids[i],
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp
        }

        response = requests.post(server_url, data=data)
        print(response.text)
        print(data)
        print(timestamp)
        time.sleep(5)
