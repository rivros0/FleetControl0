import requests
import time
import random

server_url = 'http://test0000.pythonanywhere.com/api/update_location'  # URL del server Flask hostato su PythonAnywhere
vehicle_ids = ['Punto', 'Panda', 'CarroArmatoSovietico']



while True:
    for vehicle_id in vehicle_ids:
        latitude = random.uniform(38.0, 42.0)
        longitude = random.uniform(17.0, 18.0)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        temp_acqua = random.uniform(50.0, 100.0)  # Valore di esempio per la temperatura dell'acqua
        pressione_olio = random.uniform(20.0, 80.0)  # Valore di esempio per la pressione dell'olio
        voltaggio_batteria = random.uniform(11.5, 13.5)  # Valore di esempio per il voltaggio della batteria
        contaore_motore = random.randint(1000, 5000)  # Valore di esempio per il contaore del motore
        errori = ['P0100', 'P1101']  # Lista di errori eventuali

        data = {
            'vehicle_id': vehicle_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp,
            'temp_acqua': temp_acqua,
            'pressione_olio': pressione_olio,
            'voltaggio_batteria': voltaggio_batteria,
            'contaore_motore': contaore_motore,
            'errori': errori
        }

        try:
            response = requests.post(server_url, data=data)
            response.raise_for_status()  # Raise an error for bad status codes
            print(f"Dati inviati per {vehicle_id}: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Errore nell'invio dei dati per {vehicle_id}: {e}")

    time.sleep(5)  # Intervallo di aggiornamento dei dati (5 secondi)
